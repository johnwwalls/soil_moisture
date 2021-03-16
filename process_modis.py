import os
from osgeo import gdal
import osr
import math 
import tifffile

illinois_bounds = (37.53114756912893,42.47492527271053,-91.8149898022461,-87.39462351501466)
oklahoma_bounds = (34.24527460247113,36.970101718281434,-102.9851672619629,-94.56955408752442)
def convert_to_gps(inp,outp):
    command = "gdalwarp -of GTIFF -s_srs '+proj=sinu +R=6371007.181 +nadgrids=@null +wktext' -r cubic -t_srs '+proj=longlat +datum=WGS84 +no_defs' " + inp + " " + outp
    os.system(command)
def read_to_tif(inp,outp):
    command = "gdal_translate " + inp + " " + outp
    os.system(command)
def merge(inps,outp):
    command = "gdal_merge.py -o " + outp + " "
    for inp in inps:
        command = command + inp + " "
    os.system(command)
def cut_to_box(inp,outp,bounds):
    command = "gdalwarp -te_srs EPSG:4326 -te " + str(bounds[2]) + " " + str(bounds[0]) + " " + str(bounds[3]) + " " + str(bounds[1]) + " " + inp + " " + outp
    os.system(command)
def prepare_files(inps,outp,bounds,subset):
    for inp in inps:
        read_to_tif('HDF4_EOS:EOS_GRID:"' + inp + '":MODIS_Grid_Daily_1km_LST:' + subset,inp.replace("hdf","tif"))
    merge([inp.replace("hdf","tif") for inp in inps],outp)
    convert_to_gps(outp,outp.replace(".tif","_cut.tif"))
    for inp in inps:
        os.remove(inp.replace("hdf","tif"))
    os.remove(outp)
    cut_to_box(outp.replace(".tif","_cut.tif"),outp,bounds)
    os.remove(outp.replace(".tif","_cut.tif"))
def get_soil_temperature(date, modis_tiles, folder ):
    prepare_files(modis_tiles,folder + "/illinois_lst_night_" + str(date) + ".tif", illinois_bounds, "LST_Night_1km")
    prepare_files(modis_tiles,folder + "/illinois_lst_day_" + str(date) + ".tif", illinois_bounds, "LST_Day_1km")
    prepare_files(modis_tiles,folder + "/illinois_qc_night_" + str(date) + ".tif", illinois_bounds, "QC_Night")
    prepare_files(modis_tiles,folder + "/illinois_qc_day_" + str(date) + ".tif", illinois_bounds, "QC_Day")

    prepare_files(modis_tiles,folder + "/oklahoma_lst_night_" + str(date) + ".tif", oklahoma_bounds, "LST_Night_1km")
    prepare_files(modis_tiles,folder + "/oklahoma_lst_day_" + str(date) + ".tif", oklahoma_bounds, "LST_Day_1km")
    prepare_files(modis_tiles,folder + "/oklahoma_qc_night_" + str(date) + ".tif", oklahoma_bounds, "QC_Night")
    prepare_files(modis_tiles,folder + "/oklahoma_qc_day_" + str(date) + ".tif", oklahoma_bounds, "QC_Day")
if __name__ == '__main__':
    prepare_files(["mod1.hdf","mod2.hdf"],"illinois.tif",illinois_bounds,"LST_Night_1km")
