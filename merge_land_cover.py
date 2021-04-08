import os
from osgeo import gdal
import osr
import math 
import tifffile
import numpy as np
import sys
import gdal

illinois_bounds = (37.53114756912893,42.47492527271053,-91.8149898022461,-87.39462351501466)
oklahoma_bounds = (34.24527460247113,36.970101718281434,-102.9851672619629,-94.56955408752442)
def cut_land_cover(inp, outp, bounds):
    command = "gdalwarp -te_srs EPSG:4326 -te " + str(bounds[2]) + " " + str(bounds[0]) + " " + str(bounds[3]) + " " + str(bounds[1]) + " " + inp + " " + outp
    os.system(command)
def merge(inps, outp):
    command = "gdal_merge.py -o " + outp + " "
    for inp in inps:
        command = command + inp + " "
    command = command + "-separate "
    os.system(command)
if __name__ == '__main__':
    cut_land_cover("land_cover.tif","illinois_land_cover_test.tif",illinois_bounds)
    cut_land_cover("land_cover.tif","oklahoma_land_cover_test.tif",oklahoma_bounds)
    for date in os.listdir("data"):
        print(date)
        merge(["data/" + date + "/illinois_" + date + ".tif","illinois_land_cover.tif"],"data/" + date + "/illinois_land_cover_" + date + ".tif")
        merge(["data/" + date + "/oklahoma_" + date + ".tif","oklahoma_land_cover.tif"],"data/" + date + "/oklahoma_land_cover_" + date + ".tif")
