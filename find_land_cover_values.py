import tifffile
import numpy as np
import requests

found_values = {}


payload={}
headers = {
  'Accept': 'image/geotiff',
  'Cookie': 'ROUTEID=.2'
}
img = tifffile.imread("land_cover.tif")
for i in range(len(img)):
    for j in range(len(img[i])):
        if img[i][j] not in found_values.keys():
            print(img[i][j] + " i: " + str(i) + " J: " + str(j))
            found_values[img[i][j]] = " "
print(np.unique(img))