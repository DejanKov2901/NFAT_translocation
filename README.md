# NFAT translocation 
The NFAT Translocation Analysis Tool is a Python script designed for the quantitative analysis of NFAT (nuclear factor of activated T cells) translocation into the nucleus based on fluorescence microscopy images.

# Features

- Segmentation: Utilizes simple segmentation methods to identify nuclei and NFAT proteins in fluorescence microscopy images.
- Intersection Analysis: Calculates the intersection area between the segmented nuclei and NFAT regions, providing insights into NFAT translocation into the nucleus.
- Results Table: Generates a results table summarizing the percentage of NFAT inside the nucleus for each image pair (DAPI, NFAT).


# Installation
- Install Python and IDE, see: ![Youtube tutorial](https://www.youtube.com/watch?v=XQMUWhQusjo&t=1s) 
- Install Anaconda on your computer, see ![Anaconda download page](https://www.anaconda.com/download)
- Clone Github-Repository onto local machine
- in the IDE-terminal, type "conda env create -f NFAT_Tool.yml". Then "conda activate NFAT_Tool". You should now be able to execute the main file. 

# How to Use
### Input Directory:
1. Launch the tool and provide the path to the directory containing fluorescence microscopy images in the Graphical User Interface (GUI).
![example](images/gui_image.png)

### Directory Structure:
Ensure that the image filenames follow a specific structure:
- File names should be identical for corresponding DAPI and NFAT images except for the suffix (405 for DAPI-stained nucleus, 488 for NFAT-detection)
- This is crucial for the correct function of the script! 

![example](images/directory_example.png)

### Start Analysis:
- Press the "Start" button in the GUI to initiate the analysis.
- The tool will automatically identify and pair corresponding DAPI and NFAT images based on the specified filename structure.

### Results Output:
After the analysis is complete, the tool generates a results table summarizing the percentage of NFAT translocation into the nucleus for each image pair.
Note: Users should ensure that the filenames are consistent and follow the specified structure for accurate analysis.

![example](images/results_example.png)
![example_2](images/results_example_2.png)

### Example images:
#### overlay: nucleus in purple, NFAT in green.
![example](images/230511_JMP_NFAT_basal_5_w2CF-405.tif_cell0_overlay_image.png)