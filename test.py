import tifffile
import numpy as np

img = tifffile.imread("smap_data/2020-04-19/qc_am_illinois_2020-04-19.tif")
print(np.unique(img,return_counts=True))