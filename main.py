from tkinter import Tk, filedialog
from skimage import io
import matplotlib.pyplot as plt
from Processor import Processor
import os
import pandas as pd
from GUI import NFATAnalysisGUI

def generate_sorted_filename_list(directory_path, condition):
    # Get a list of all files in the directory
    file_list = [directory_path + '/' + f for f in os.listdir(directory_path) if f.lower().endswith('.tif') and not f.startswith(".") and condition in f]
    file_list = sorted(file_list)
    return file_list

# Create an empty DataFrame
results = pd.DataFrame(columns=["nucleus (DAPI) image", "NFAT image", "cell_index","percentage of NFAT in nucleus"])


def main():
    gui = NFATAnalysisGUI()
    gui.run_gui()
    input_directory = gui.input_directory

    if not input_directory:
        print("No directory selected. Exiting.")
        return

    brightfield_files = generate_sorted_filename_list(input_directory, 'Brightfield')
    channel_405_files = generate_sorted_filename_list(input_directory, 'CF-405')  # Nucleus, DAPI staining
    channel_488_files = generate_sorted_filename_list(input_directory, 'CF-488')  # NFAT

    for elem in list(zip(brightfield_files, channel_405_files, channel_488_files)):
        image_processor = Processor(elem[0], elem[1], elem[2])
        nuclei_rois = image_processor.find_ROIs()
        image_processor.create_cell_images(nuclei_rois)
        image_processor.analyze_nfat_translocation()
        image_processor.add_results(results)

    save_path = input_directory + '/results/'
    os.makedirs(save_path, exist_ok=True)
    with pd.ExcelWriter(save_path + "NFAT_translocation_results.xlsx") as writer:
        results.to_excel(writer, index=False)

if __name__ == "__main__":
    main()