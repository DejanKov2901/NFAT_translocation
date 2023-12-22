from skimage import io
from Cell_Image import CellImage
import os
from Segmentation import Nucleus_Segmentation, NFAT_Segmentation
import matplotlib.pyplot as plt

class Processor:
    def __init__(self, brightfield_channel_path, channel_405_path, channel_488_path):
        self.cell_list = list()
        self.brightfield_channel_image = io.imread(brightfield_channel_path)
        self.channel_405_image = io.imread(channel_405_path)  # Nucleus, DAPI staining
        self.channel_405_filename = os.path.basename(channel_405_path)
        self.channel_488_image = io.imread(channel_488_path)  # NFAT
        self.channel_488_filename = os.path.basename(channel_488_path)
        self.nuclei_segmentation = Nucleus_Segmentation()
        self.nfat_segmentation = NFAT_Segmentation()

    def find_ROIs(self):
        labeled_nuclei = self.nuclei_segmentation.segment_nuclei(self.channel_405_image)
        self.channel_405_image = labeled_nuclei
        nuclei_rois = self.nuclei_segmentation.generate_nucleus_rois(labeled_nuclei)
        return nuclei_rois

    def create_cell_images(self, nuclei_rois):
        for index, roi in enumerate(nuclei_rois):
            minr, minc, maxr, maxc = roi
            nucleus_image = self.channel_405_image[minr:maxr, minc:maxc]
            nucleus_image[nucleus_image > 0] = 1
            nfat_image = self.channel_488_image[minr:maxr, minc:maxc]

            cell_image = CellImage(nucleus_image, nfat_image, self.channel_405_filename, self.channel_488_filename, index)
            self.cell_list.append(cell_image)

    def analyze_nfat_translocation(self):
        for cell in self.cell_list:
            cell.nfat_image = self.nfat_segmentation.segment_NFAT(cell.nfat_image)
            cell.measure_NFAT_translocation()

    def add_results(self, results):
        for cell in self.cell_list:

            nucleus_channel_file = cell.nucleus_channel_filename
            nfat_channel_filename = cell.nfat_channel_filename
            percentage_nfat_in_nucleus = cell.nfat_in_nucleus

            results.loc[len(results.index)] = [nucleus_channel_file, nfat_channel_filename, cell.index, percentage_nfat_in_nucleus]



