from skimage import io
import matplotlib.pyplot as plt
import numpy as np

class CellImage:
    def __init__(self, nucleus_image, nfat_image, nucleus_channel_filename, nfat_channel_filename, index):
        self.nucleus_image = nucleus_image
        self.nfat_image = nfat_image
        self.nfat_in_nucleus = 0.0  # min 0.0, max 1.0
        self.nucleus_channel_filename = nucleus_channel_filename
        self.nfat_channel_filename = nfat_channel_filename
        self.index = index

    def measure_NFAT_translocation(self):
        # Calculate the intersection of the nucleus and protein masks
        intersection_mask = np.logical_and(self.nucleus_image, self.nfat_image)

        # Calculate percentage inside the nucleus
        self.nfat_in_nucleus = np.sum(intersection_mask) / np.sum(self.nfat_image) * 100