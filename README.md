# NFAT translocation
[![DOI](https://zenodo.org/badge/734651356.svg)](https://zenodo.org/doi/10.5281/zenodo.10511337)

## About 
The NFAT Translocation Analysis Tool is a Python script designed for the quantitative analysis of NFAT (nuclear factor of activated T cells) translocation into the nucleus based on fluorescence microscopy images.

## Features

- Segmentation: Utilizes simple segmentation methods to identify the nuclei and NFAT proteins in fluorescence microscopy images.
- Intersection Analysis: Calculates the intersection area between the segmented nuclei and NFAT areas, providing insights into NFAT translocation into the nucleus.
- Results Table: Generates a results table summarizing the percentage of NFAT inside the nucleus for each image pair (DAPI stained nucleus, NFAT).


## Installation
1. If Python is already installed, skip to 3. Else: Install Python and IDE, see: [Youtube tutorial](https://www.youtube.com/watch?v=XQMUWhQusjo&t=1s) 
2. Install Anaconda on your computer, see [Anaconda download page](https://www.anaconda.com/download)
3. Clone Github-Repository to local machine
4. in the IDE-terminal, type "conda env create -f NFAT_Tool.yml". Then "conda activate NFAT_Tool". You should now be able to execute the main file. 

## How to Use
### Input Directory:
1. Launch the tool and provide the path to the directory containing fluorescence microscopy images in the Graphical User Interface (GUI).
![example](images/gui_image.png)

### Directory Structure:
Ensure that the image filenames follow a specific structure:
- File names should be identical for corresponding DAPI and NFAT images except for the suffix
  - In the example, the difference lies only in "w2CF-405" (for imaging of DAPI-stained nuclei) and "w3CF-488" (for NFAT-detection) (cameras from microscope). This enables to match the corresponding files to each other.
- This is crucial for the correct function of the script! 

![example](images/directory_structure_new.png)

### Start Analysis:
- Press the "Start" button in the GUI to initiate the analysis.
- For each file, define rectangular regions of interest. 
  - click on "Add ROI"
  - to generate a ROI, click and release the left mouse button from the top left to the bottom right corner of the ROI, for example
  - repeat these steps for each cell in the file
  - If you're done with the file, click on "Continue with next image"

![example](images/cell_selection.png)

### Results Output:
After the analysis is completed, the tool generates a results table summarizing the percentage of NFAT translocation into the nucleus for each image pair.
You can find the results directory inside the original directory.

For each nucleus-NFAT image-pair, five images are generated: 
- labeled nucleus image
- raw but cropped nucleus image
- NFAT image (after background subtraction)
- labeled NFAT image
- RGB: overlay image (NFAT and nucleus)

To open these images in Fiji/ImageJ, use the bioformats importer. 

![example](images/results_structure.png)


The Excel table looks like this, for example: 
![example_2](images/results_example_2.png)

### Example images:
#### overlay: nucleus in purple, NFAT in green.
![example](images/230511_JMP_NFAT_basal_5_w2CF-405.tif_cell0_overlay_image.png)


## License
This code runs under the Apache 2.0 license.

## References and citing 
If you use code and this leads to a publication, please cite the DOI above.