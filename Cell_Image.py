from skimage import io
import matplotlib.pyplot as plt
import numpy as np

class CellImage:
    def __init__(self, nucleus_image_labeled, nucleus_image_raw, nfat_image_background_subtracted, nucleus_channel_filename, nfat_channel_filename, index):
        self.nucleus_image_labeled = nucleus_image_labeled
        self.nucleus_image_raw = nucleus_image_raw

        self.nfat_image_labeled = None
        self.nfat_image_background_subtracted = nfat_image_background_subtracted

        self.nfat_in_nucleus = 0.0  # min 0.0, max 1.0
        self.nucleus_channel_filename = nucleus_channel_filename
        self.nfat_channel_filename = nfat_channel_filename
        self.index = index

    def measure_NFAT_translocation(self):
        # Calculate the intersection of the nucleus and protein masks
        intersection_mask = np.logical_and(self.nucleus_image_labeled, self.nfat_image_labeled)

        # Calculate percentage inside the nucleus
        self.nfat_in_nucleus = (np.sum(intersection_mask) / np.sum(self.nfat_image_labeled)) * 100