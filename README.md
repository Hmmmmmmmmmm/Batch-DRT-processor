# Unfinished
# TODO
[] Update installation guides
[] Check for repo name
[] Update citation info

# DRT-batch Processor

A Python-based automated pipeline for processing Electrochemical Impedance Spectroscopy (EIS) data from CHI workstations. This tool streamlines the workflow from raw data trimming to Distribution of Relaxation Times (DRT) calculation and final data aggregation.

## Features

1.  **Automated Trimming**: Strips headers and standardizes raw `.txt` files, currently only supporting CHI electrochemical workstations.
2.  **Batch DRT Calculation**: Utilizes `pyDRTtools` to calculate Tau vs. Gamma distribution for all files in sequence.
3.  **Matrix Aggregation**: Compiles all processed DRT results into a single master `.csv` matrix for easy plotting.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Hmmmmmmmmmm/Batch-DRT-processor.git
    cd Batch-DRT-processor
    ```

2.  **Create a virtual environment (Recommended)**:
    ```
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Prepare your data**:
    Create a project folder. Inside it, create a subfolder named `0_Raw_Input` and place your raw CHI `.txt` files there.

    ```text
    Project_Folder/
    └── 0_Raw_Input/
        ├── file1.txt
        ├── file2.txt
        └── ...
    ```

2.  **Configure the script**:
    Open `drt_batch_processor.py` and update the `working_directory` variable at the bottom of the file to point to your `Project_Folder`.

3.  **Run the pipeline**:
    ```bash
    python drt_batch_processor.py
    ```

4.  **Output**:
    The script will generate the following folders:
    * `1_Trimmed_Data`: Cleaned EIS data.
    * `2_DRT_Output`: Individual DRT calculation results (Tau/Gamma).
    * `3_Summary_Matrix`: A single `Master_DRT_Matrix.csv` containing aligned data for all samples.

## Citation

If you use this tool in your research, please cite:
* **Code**: [Your Name]. (2025). CHI-DRT Batch Processor [Software]. Zenodo. https://doi.org/10.5281/zenodo.xxxxxx
* **Method**: Wan, T. H., Saccoccio, M., Chen, C., & Ciucci, F. (2015). Influence of the discretization methods on the distribution of relaxation times deconvolution: implementing radial basis functions with DRTtools. *Electrochimica Acta*, 184, 483-499.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
