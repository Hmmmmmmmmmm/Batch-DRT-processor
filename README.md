# Unfinished
# TODO
[] Update citation info

# DRT-batch Processor

A Python-based automated pipeline for processing Electrochemical Impedance Spectroscopy (EIS) data from CHI workstations. This tool streamlines the workflow from raw data trimming to Distribution of Relaxation Times (DRT) calculation and final data aggregation.

## Features

1.  **Automated Trimming**: Strips headers and standardizes raw `.txt` files, currently only supporting CHI electrochemical workstations.
2.  **Batch DRT Calculation**: Utilizes `pyDRTtools` to calculate Tau vs. Gamma distribution for all files in sequence.
3.  **Matrix Aggregation**: Compiles all processed DRT results into a single master `.csv` matrix for easy plotting.

## Installation

1.  **Download the code**:
    Right click the file named `drt_batch_processor.py` and save it to your working project folder.

2.  **Installation of pyDRTtools library and dependencies using conda**:
    In your terminal, run the following codes after installation of conda.
    ```
    conda create -n DRT python=3.11
    conda activate DRT
    conda install -c pip ipython pandas matplotlib scikit-learn spyder cvxopt pyqt
    pip install pyDRTtools
    ```
    After the above commands, verify your installation by toggling the GUI of pyDRTtools by
    ```
    !launchGUI
    ```
    If a GUI instance popped up, your installation should be fine. 

## Usage for batch process

1.  **Prepare your data**:
    Create a new data folder, name it with your experiement details. Inside it, create a subfolder named `0_Raw_Input` and place your raw CHI `.txt` files there.
    (Or if you run this script with a blank folder, it will create a new `0_Raw_Input` folder for you)
    ```text
    Data_Folder/
    └── 0_Raw_Input/
        ├── file1.txt
        ├── file2.txt
        └── ...
    ```

2.  **Configure the script**:
    Open `drt_batch_processor.py` and update the `working_directory` variable at the bottom of the file to point to your `Data_Folder`.

3.  **Run the pipeline**:
    In your terminal with DRT virtual environment activated, run
    ```bash
    python drt_batch_processor.py
    ```

5.  **Output**:
    The script will generate the following folders:
    * `1_Trimmed_Data`: Cleaned EIS data.
    * `2_DRT_Output`: Individual DRT calculation results (Tau/Gamma).
    * `3_Summary_Matrix`: A single `Master_DRT_Matrix.csv` containing aligned data for all samples.

## Citation

If you use this tool in your research, please cite:
* **Code**: [Your Name]. (2025). CHI-DRT Batch Processor [Software]. Zenodo. https://doi.org/10.5281/zenodo.xxxxxx
* **Method**: Wan, T. H., Saccoccio, M., Chen, C., & Ciucci, F. (2015). Influence of the discretization methods on the distribution of relaxation times deconvolution: implementing radial basis functions with DRTtools. *Electrochimica Acta*, 184, 483-499.

## Links
pyDRTtools: https://github.com/ciuccislab/pyDRTtools

## License

This project is licensed under the MIT License - see the LICENSE file for details.
