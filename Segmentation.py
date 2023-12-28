import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops
from skimage import io, filters, measure
from skimage.segmentation import clear_border
from scipy import ndimage
from skimage.restoration import rolling_ball

class Nucleus_Segmentation:

    def preprocess_image(self, image):
        # Apply Gaussian blur
        blurred = filters.gaussian(image, sigma=2)

        # Adaptive thresholding
        thresholded = blurred > filters.threshold_otsu(blurred)

        # Fill holes in the binary image
        filled_nucleus_binary = ndimage.binary_fill_holes(thresholded)

        return filled_nucleus_binary


    def segment_nuclei(self, image):
        # Preprocess the image
        preprocessed = self.preprocess_image(image)

        # Clear border
        cleared = clear_border(preprocessed)

        # Label connected components
        labeled_nuclei = measure.label(cleared)
        return labeled_nuclei

    def generate_nucleus_rois(self, labels, margin=50):
        rois = []

        # Get region properties of segmented nuclei
        regions = regionprops(labels)

        # filter out small regions
        regions = [r for r in regions if r.area > 100*100]

        for region in regions:
            minr, minc, maxr, maxc = region.bbox

            # Calculate adjusted margin based on proximity to image boundaries
            minr_margin = min(minr, margin)
            minc_margin = min(minc, margin)
            maxr_margin = min(labels.shape[0] - maxr, margin)
            maxc_margin = min(labels.shape[1] - maxc, margin)

            # Adjust bounding box based on the calculated margins
            minr = max(0, minr - minr_margin)
            minc = max(0, minc - minc_margin)
            maxr = min(labels.shape[0], maxr + maxr_margin)
            maxc = min(labels.shape[1], maxc + maxc_margin)

            rois.append((minr, minc, maxr, maxc))

        return rois

class NFAT_Segmentation:
    def preprocess_image(self, image):
        # Apply Gaussian blur
        blurred = filters.gaussian(image, sigma=1)

        threshold = np.percentile(blurred, 85)
        thresholded = blurred > threshold

        return thresholded

    def segment_NFAT(self, image):
        # Preprocess the image
        nfat_image = self.preprocess_image(image)

        # maybe use deep learning based segmentation methods? U-Net

        # label image
        nfat_image = measure.label(nfat_image)

        nfat_image[nfat_image > 0] = 1
        return nfat_image