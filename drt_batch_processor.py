import os
import pandas as pd
import numpy as np
import re
from pyDRTtools.runs import EIS_object, simple_run

class DRTBatchProcessor:
    def __init__(self, root_folder):
        """
        Initializes the processor with a root folder.
        Automatically creates subfolders for each processing step.
        """
        self.root = root_folder
        self.raw_dir = os.path.join(root_folder, "0_Raw_Input")
        self.trimmed_dir = os.path.join(root_folder, "1_Trimmed_Data")
        self.drt_out_dir = os.path.join(root_folder, "2_DRT_Output")
        self.matrix_dir = os.path.join(root_folder, "3_Summary_Matrix")
        
        # Ensure the raw input directory exists
        if not os.path.exists(self.raw_dir):
            os.makedirs(self.raw_dir)
            print(f"⚠️ Created input folder at: {self.raw_dir}")
            print("Please place your raw .txt files in this folder and re-run.")
            return

        # Create output directories
        for d in [self.trimmed_dir, self.drt_out_dir, self.matrix_dir]:
            os.makedirs(d, exist_ok=True)

    def numeric_sort_key(self, s):
        """
        Sorts filenames numerically (e.g., 1, 2, 10) rather than alphabetically (1, 10, 2).
        """
        nums = re.findall(r"(\d+)", s)
        if nums:
            return (0, tuple(int(n) for n in nums), s.lower())
        return (1, (), s.lower())

    def step_1_trim_files(self):
        """
        Reads raw CHI txt files, skips 18 header lines, removes extra columns,
        and saves clean Freq/Z'/Z'' data.
        """
        print(f"\n--- Step 1: Trimming CHI Files from {os.path.basename(self.raw_dir)} ---")
        files = [f for f in os.listdir(self.raw_dir) if f.lower().endswith('.txt')]
        
        if not files:
            print("No .txt files found in 0_Raw_Input.")
            return

        for fname in files:
            path = os.path.join(self.raw_dir, fname)
            
            # Skip if file starts with "trimmed_" to avoid re-processing output
            if fname.startswith('trimmed_'):
                continue

            try:
                # Attempt to read standard CHI format (skip 18 header lines)
                try:
                    df = pd.read_csv(path, sep=None, engine='python', header=None, skiprows=18, on_bad_lines='skip')
                except:
                    # Fallback to whitespace separation
                    df = pd.read_csv(path, sep=r'\s+', header=None, skiprows=18, on_bad_lines='skip')

                # Drop columns 3 and 4 (indices 3, 4) if they exist
                if df.shape[1] > 4:
                    df.drop(df.columns[[3, 4]], axis=1, inplace=True)
                elif df.shape[1] > 3:
                    df.drop(df.columns[[3]], axis=1, inplace=True)
                
                # Check if we have enough columns left (Freq, Z', Z'')
                if df.shape[1] < 3:
                    print(f"Skipping {fname}: Not enough columns found.")
                    continue

                out_name = f"trimmed_{fname}"
                out_path = os.path.join(self.trimmed_dir, out_name)
                df.to_csv(out_path, sep='\t', index=False, header=False)
                print(f"Trimmed: {fname}")

            except Exception as e:
                print(f"Failed to read {fname}: {e}")

    def step_2_calculate_drt(self):
        """
        Reads trimmed files and runs pyDRTtools calculation.
        Saves Tau vs Gamma.
        """
        print(f"\n--- Step 2: Calculating DRT in {os.path.basename(self.drt_out_dir)} ---")
        files = sorted([f for f in os.listdir(self.trimmed_dir) if f.endswith(".txt")], key=self.numeric_sort_key)
        
        if not files:
            print("No trimmed files found. Did Step 1 run?")
            return

        for file in files:
            try:
                # Read trimmed data (Tab delimited, no header)
                data = pd.read_csv(os.path.join(self.trimmed_dir, file), delimiter='\t', header=None)
                freq = data[0].values  # Col 1: Frequency
                Zre = data[1].values   # Col 2: Z real
                Zim = data[2].values   # Col 3: Z imag

                # Run DRT
                eis = EIS_object(freq, Zre, Zim)
                out_simple = simple_run(eis)
                
                # Extract Tau and Gamma
                tau = out_simple.out_tau_vec
                gamma = out_simple.gamma
                
                out = pd.DataFrame({"tau": tau, "gamma": gamma})
                
                # Create clean output filename
                clean_name = file.replace('trimmed_', '')
                out_name = f"DRT_{clean_name}"
                
                out.to_csv(os.path.join(self.drt_out_dir, out_name), index=False)
                print(f"Calculated DRT: {clean_name}")
                
            except Exception as e:
                print(f"Error calculating DRT for {file}: {e}")

    def step_3_generate_matrix(self):
        """
        Aggregates all individual DRT results into a single Matrix CSV.
        """
        print(f"\n--- Step 3: Generating Summary Matrix in {os.path.basename(self.matrix_dir)} ---")
        input_files = sorted([f for f in os.listdir(self.drt_out_dir) if f.endswith('.csv') or f.endswith('.txt')], key=self.numeric_sort_key)
        
        if not input_files:
            print("No DRT output files found to aggregate.")
            return

        first_tau_axis = None
        gamma_columns = []
        file_headers = []

        for fname in input_files:
            df = pd.read_csv(os.path.join(self.drt_out_dir, fname))
            
            # Assume Col 0 is 'tau' and Col 1 is 'gamma'
            current_tau = df.iloc[:, 0].values
            current_gamma = df.iloc[:, 1].values

            # Initialize with the first file's Tau axis
            if first_tau_axis is None:
                first_tau_axis = current_tau
                file_headers.append("Tau")
            
            # Data Length Alignment
            # If current file is shorter/longer than the first file, crop or pad
            if len(current_gamma) != len(first_tau_axis):
                # Crop to minimum length to ensure matrix fits
                min_len = min(len(current_gamma), len(first_tau_axis))
                current_gamma = current_gamma[:min_len]
                if len(first_tau_axis) > min_len:
                    # Update master axis if it was longer
                    first_tau_axis = first_tau_axis[:min_len]
                    # Also crop previously stored columns
                    gamma_columns = [col[:min_len] for col in gamma_columns]

            gamma_columns.append(current_gamma)
            
            # Clean header name
            clean_header = fname.replace("DRT_", "").replace(".csv", "").replace(".txt", "")
            file_headers.append(clean_header)

        if first_tau_axis is not None and gamma_columns:
            # Stack Tau + All Gamma columns
            matrix_data = np.column_stack([first_tau_axis] + gamma_columns)
            
            result_df = pd.DataFrame(matrix_data, columns=file_headers)
            
            output_file = os.path.join(self.matrix_dir, 'Master_DRT_Matrix.csv')
            result_df.to_csv(output_file, index=False)
            
            print(f"✅ Matrix created with shape: {result_df.shape}")
            print(f"Saved to: {output_file}")
        else:
            print("Failed to stack data. Check input file consistency.")

# --- Main Execution ---
if __name__ == "__main__":
    # ==========================================
    # USER SETTING: PATH CONFIGURATION
    # ==========================================
    # Replace this string with the path to your project folder
    working_directory = '/Users/tianrao/Desktop/DRTtools-batch/data/'
    
    # Run the pipeline
    processor = DRTBatchProcessor(working_directory)
    
    # You can comment out steps if you only want to run specific parts
    processor.step_1_trim_files()
    processor.step_2_calculate_drt()
    processor.step_3_generate_matrix()