from Cell_Image import CellImage
import os
from Segmentation import Nucleus_Segmentation, NFAT_Segmentation
from cell_selection_tool import ImageViewer
import tkinter as tk
from tkinter import ttk
from skimage import io, measure, morphology
from scipy.ndimage import binary_fill_holes
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Processor:
    def __init__(self, channel_405_path, channel_488_path, save_path, brightfield_image_path):
        self.cell_list = list()
        self.channel_405_image_labeled = None
        self.channel_405_image = io.imread(channel_405_path)  # Nucleus, DAPI staining
        self.channel_405_filename = os.path.basename(channel_405_path)

        self.channel_488_image = io.imread(channel_488_path)  # NFAT
        self.channel_488_filename = os.path.basename(channel_488_path)

        self.nuclei_segmentation = Nucleus_Segmentation()
        self.nfat_segmentation = NFAT_Segmentation()
        self.save_path = save_path
        self.channel_488_image_background_subtracted = None
        width = len(self.channel_405_image[0])
        height = len(self.channel_405_image)

        self.brightfield_image = io.imread(brightfield_image_path)

        self.image_viewer = ImageViewer(self.channel_405_image, width, height, self.brightfield_image)

    def find_ROIs(self):
        self.channel_405_image_labeled = self.nuclei_segmentation.segment_nuclei(self.channel_405_image)
        nuclei_rois = self.nuclei_segmentation.generate_nucleus_rois(self.channel_405_image_labeled)
        return nuclei_rois

    def label_nuclei(self):
        for cell in self.cell_list:
            nucleus_image = cell.nucleus_image_raw
            self.display_thresholding_gui(nucleus_image, cell)

    def display_thresholding_gui(self, nucleus_image, cell):
        root = tk.Tk()
        root.title("Manual Nucleus Thresholding")

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(nucleus_image, cmap='gray')
        ax.axis('off')
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        def update_threshold(val):
            thresh = int(val)
            binary = nucleus_image > thresh
            ax.imshow(binary, cmap='gray')
            canvas.draw()

        slider = tk.Scale(root, from_=np.max(nucleus_image), to=np.min(nucleus_image), orient=tk.HORIZONTAL, length=500, command=update_threshold)
        slider.pack()

        def save_and_exit():
            thresh = int(slider.get())
            binary = nucleus_image > thresh

            # Remove singular pixels
            binary = morphology.remove_small_objects(binary, min_size=50)

            # Fill holes in the binary image
            binary = binary_fill_holes(binary)

            labeled_nucleus = measure.label(binary)
            labeled_nucleus[labeled_nucleus>1] = 1
            cell.nucleus_image_labeled = labeled_nucleus
            root.destroy()

        save_button = ttk.Button(root, text="Save and Next", command=save_and_exit)
        save_button.pack()

        def cancel_and_exit():
            root.destroy()

        cancel_button = ttk.Button(root, text="Cancel", command=cancel_and_exit)
        cancel_button.pack()

        root.mainloop()

    def select_cells(self):
        self.image_viewer.run_mainloop()
        return self.image_viewer.return_rois()

    def create_cell_images(self, nuclei_rois):
        for index, roi in enumerate(nuclei_rois):
            minr, minc, maxr, maxc = roi
            # nucleus_image_labeled = self.channel_405_image_labeled[minr:maxr, minc:maxc]
            # nucleus_image_labeled[nucleus_image_labeled > 0] = 1
            nucleus_image_raw = self.channel_405_image[minr:maxr, minc:maxc]
            nfat_image_background_subtracted = self.channel_488_image_background_subtracted[minr:maxr, minc:maxc]

            cell_image = CellImage(None, nucleus_image_raw, nfat_image_background_subtracted, self.channel_405_filename, self.channel_488_filename, index)
            self.cell_list.append(cell_image)

    def subtract_background_NFAT_image(self):
        # Estimate the background
        background = np.percentile(self.channel_488_image, 50)

        # subtract the background
        self.channel_488_image_background_subtracted = np.maximum(self.channel_488_image - background, 0) #.astype(int)
        pass



    def analyze_nfat_translocation(self):
        for cell in self.cell_list:
            cell.nfat_image_labeled = self.nfat_segmentation.segment_NFAT(cell.nfat_image_background_subtracted)
            cell.measure_NFAT_translocation()

    def add_results(self, results):
        for cell in self.cell_list:

            nucleus_channel_file = cell.nucleus_channel_filename
            nfat_channel_filename = cell.nfat_channel_filename
            percentage_nfat_in_nucleus = cell.nfat_in_nucleus

            results.loc[len(results.index)] = [nucleus_channel_file, nfat_channel_filename, cell.index, percentage_nfat_in_nucleus]

    def save_cell_images(self):
        for i, cell in enumerate(self.cell_list):
            nucleus_image_raw = cell.nucleus_image_raw
            nucleus_image_labeled = cell.nucleus_image_labeled
            nfat_image_background_subtracted = cell.nfat_image_background_subtracted
            nfat_image_labeled = cell.nfat_image_labeled

            save_path_cell = self.save_path + self.channel_405_filename[:len(self.channel_405_filename) - 8] + '/cell_' + str(i) + '/'
            os.makedirs(save_path_cell, exist_ok=True)
            io.imsave(save_path_cell + self.channel_405_filename + '_cell' + str(cell.index) + '_nucleus_image_raw.tif', nucleus_image_raw, check_contrast=False)
            io.imsave(save_path_cell + self.channel_405_filename + '_cell' + str(cell.index) + '_nucleus_image_labeled.tif', nucleus_image_labeled, check_contrast=False)
            io.imsave(save_path_cell + self.channel_488_filename + '_cell' + str(cell.index) + '_nfat_image_background_subtracted.tif', nfat_image_background_subtracted, check_contrast=False)
            io.imsave(save_path_cell + self.channel_488_filename + '_cell' + str(cell.index) + '_nfat_image_labeled.tif', nfat_image_labeled, check_contrast=False)

            # Define colors for the nucleus and NFAT
            nucleus_color = [0.5, 0, 0.5]  # Purple
            nfat_color = [0, 1, 0]  # Green

            # Create an empty RGB image
            overlay_img = np.zeros((nucleus_image_labeled.shape[0], nucleus_image_labeled.shape[1], 3))

            # Assign colors to the nucleus and NFAT regions
            overlay_img[:, :, 0] = nucleus_image_labeled * nucleus_color[0] + nfat_image_labeled * nfat_color[0]  # Red channel
            overlay_img[:, :, 1] = nucleus_image_labeled * nucleus_color[1] + nfat_image_labeled * nfat_color[1]  # Green channel
            overlay_img[:, :, 2] = nucleus_image_labeled * nucleus_color[2] + nfat_image_labeled * nfat_color[2]  # Blue channel

            # Display the overlay image
            # plt.imshow(overlay_img)
            # plt.axis('off')  # Turn off axis labels
            # plt.show()

            io.imsave(save_path_cell + self.channel_405_filename + '_cell' + str(cell.index) + '_overlay_image.tif', overlay_img, check_contrast=False)
