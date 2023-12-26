from skimage import io
from Cell_Image import CellImage
import os
from Segmentation import Nucleus_Segmentation, NFAT_Segmentation
import matplotlib.pyplot as plt
import numpy as np

class Processor:
    def __init__(self, brightfield_channel_path, channel_405_path, channel_488_path, save_path):
        self.cell_list = list()
        self.brightfield_channel_image = io.imread(brightfield_channel_path)
        self.channel_405_image_labeled = None
        self.channel_405_image = io.imread(channel_405_path)  # Nucleus, DAPI staining
        self.channel_405_filename = os.path.basename(channel_405_path)

        self.channel_488_image = io.imread(channel_488_path)  # NFAT
        self.channel_488_filename = os.path.basename(channel_488_path)

        self.nuclei_segmentation = Nucleus_Segmentation()
        self.nfat_segmentation = NFAT_Segmentation()
        self.save_path = save_path

    def find_ROIs(self):
        self.channel_405_image_labeled = self.nuclei_segmentation.segment_nuclei(self.channel_405_image)
        nuclei_rois = self.nuclei_segmentation.generate_nucleus_rois(self.channel_405_image_labeled)
        return nuclei_rois

    def create_cell_images(self, nuclei_rois):
        for index, roi in enumerate(nuclei_rois):
            minr, minc, maxr, maxc = roi
            nucleus_image_labeled = self.channel_405_image_labeled[minr:maxr, minc:maxc]
            nucleus_image_labeled[nucleus_image_labeled > 0] = 1
            nucleus_image_raw = self.channel_405_image[minr:maxr, minc:maxc]
            nfat_image_raw = self.channel_488_image[minr:maxr, minc:maxc]

            cell_image = CellImage(nucleus_image_labeled, nucleus_image_raw, nfat_image_raw, self.channel_405_filename, self.channel_488_filename, index)
            self.cell_list.append(cell_image)

    def analyze_nfat_translocation(self):
        for cell in self.cell_list:
            cell.nfat_image_labeled = self.nfat_segmentation.segment_NFAT(cell.nfat_image_raw)
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
            nfat_image_raw = cell.nfat_image_raw
            nfat_image_labeled = cell.nfat_image_labeled

            io.imsave(self.save_path + '/' + self.channel_405_filename + '_cell' + str(cell.index) + '_nucleus_image_raw.tif', nucleus_image_raw, check_contrast=False)
            io.imsave(self.save_path + '/' + self.channel_405_filename + '_cell' + str(cell.index) + '_nucleus_image_labeled.tif', nucleus_image_labeled, check_contrast=False)
            io.imsave(self.save_path + '/' + self.channel_488_filename + '_cell' + str(cell.index) + '_nfat_image_raw.tif', nfat_image_raw, check_contrast=False)
            io.imsave(self.save_path + '/' + self.channel_488_filename + '_cell' + str(cell.index) + '_nfat_image_labeled.tif', nfat_image_labeled, check_contrast=False)

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

            io.imsave(self.save_path + '/' + self.channel_405_filename + '_cell' + str(cell.index) + '_overlay_image.tif', overlay_img, check_contrast=False)
