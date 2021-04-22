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
missouri_bounds = (37.061571,40.602820,-95.007699,-91.239652)
def convert_to_gps(inp,outp,qc):
    res = "average"
    if qc:
        res = "mode"
    command = "gdalwarp -of GTIFF -r " + res + " -s_srs '+proj=sinu +R=6371007.181 +nadgrids=@null +wktext' -r cubic -t_srs '+proj=longlat +datum=WGS84 +no_defs' " + inp + " " + outp
    os.system(command)
def read_to_tif(inp,outp,qc):
    command = "gdal_translate " + inp + " " + outp.replace(".tif","temp.tif")
    os.system(command)
    if qc:
        command = "gdal_calc.py -A " + outp.replace(".tif","temp.tif") + " --outfile=" + outp + ' --calc="A*1"'
    else:
        command = "gdal_calc.py -A " + outp.replace(".tif","temp.tif") + " --outfile=" + outp + ' --calc="A*1" --NoDataValue=0'
    os.system(command)
    os.remove(outp.replace(".tif","temp.tif"))
def warp(inp,outp,width,height,qc):
    res = "average"
    if qc:
        res = "mode"
    command = "gdalwarp -r " + res + " -ts " + str(width) + " " + str(height) + " " + inp + " " + outp
    os.system(command)
def merge(inps,outp):
    command = "gdal_merge.py -o " + outp + " "
    for inp in inps:
        command = command + inp + " "
    os.system(command)
def cut_to_box(inp,outp,bounds):
    command = "gdalwarp -te_srs EPSG:4326 -te " + str(bounds[2]) + " " + str(bounds[0]) + " " + str(bounds[3]) + " " + str(bounds[1]) + " " + inp + " " + outp
    os.system(command)
def add_land_cover_no_data(inp,outp,state):
    command = "gdal_calc.py -A " + inp + " -B " + state+"_land_cover_1km.tif" + " --outfile=" + outp + ' --calc="((B==14)|(B==18)|(B==19))*A" --NoDataValue=0'
    os.system(command)
def prepare_files(inps,outp,bounds,subset,qc,width,height,state):
    for inp in inps:
        read_to_tif('HDF4_EOS:EOS_GRID:"' + inp + '":MODIS_Grid_Daily_1km_LST:' + subset,inp.replace("hdf","tif"),qc)
    merge([inp.replace("hdf","tif") for inp in inps],outp.replace(".tif","_pre.tif"))
    ds = gdal.Open( outp.replace(".tif","_pre.tif"),1) # The 1 means that you are opening the file to edit it)
    rb = ds.GetRasterBand(1) #assuming your raster has 1 band. 
    if not qc:
        rb.SetNoDataValue(0)
    rb= None 
    ds = None
    convert_to_gps(outp.replace(".tif","_pre.tif"),outp.replace(".tif","_cut.tif"),qc)
    for inp in inps:
        os.remove(inp.replace("hdf","tif"))
    #os.remove(outp)
    cut_to_box(outp.replace(".tif","_cut.tif"),outp.replace(".tif","_cut2.tif"),bounds)
    add_land_cover_no_data(outp.replace(".tif","_cut2.tif"),outp.replace(".tif","_cut3.tif"),state)
    warp(outp.replace(".tif","_cut3.tif"),outp,width,height,qc)
    os.remove(outp.replace(".tif","_cut.tif"))
    os.remove(outp.replace(".tif","_cut2.tif"))
    os.remove(outp.replace(".tif","_cut3.tif"))
    os.remove(outp.replace(".tif","_pre.tif"))
def get_soil_temperature(date, modis_tiles, folder ):
    prepare_files(modis_tiles,folder + "/illinois_qc_night_" + str(date) + ".tif", illinois_bounds, "QC_Night",True,48,55,"illinois")
    prepare_files(modis_tiles,folder + "/illinois_qc_day_" + str(date) + ".tif", illinois_bounds, "QC_Day",True,48,55,"illinois")
    prepare_files(modis_tiles,folder + "/illinois_lst_night_" + str(date) + ".tif", illinois_bounds, "LST_Night_1km",False,48,55,"illinois")
    prepare_files(modis_tiles,folder + "/illinois_lst_day_" + str(date) + ".tif", illinois_bounds, "LST_Day_1km",False,48,55,"illinois")
    
    prepare_files(modis_tiles,folder + "/oklahoma_qc_night_" + str(date) + ".tif", oklahoma_bounds, "QC_Night",True,91,32,"oklahoma")
    prepare_files(modis_tiles,folder + "/oklahoma_qc_day_" + str(date) + ".tif", oklahoma_bounds, "QC_Day",True,91,32,"oklahoma")
    prepare_files(modis_tiles,folder + "/oklahoma_lst_night_" + str(date) + ".tif", oklahoma_bounds, "LST_Night_1km",False,91,32,"oklahoma")
    prepare_files(modis_tiles,folder + "/oklahoma_lst_day_" + str(date) + ".tif", oklahoma_bounds, "LST_Day_1km",False,91,32,"oklahoma")
    """
    prepare_files(modis_tiles,folder + "/missouri_lst_night_" + str(date) + ".tif", missouri_bounds, "LST_Night_1km",False,91,32)
    prepare_files(modis_tiles,folder + "/missouri_lst_day_" + str(date) + ".tif", missouri_bounds, "LST_Day_1km",False,91,32)
    prepare_files(modis_tiles,folder + "/missouri_qc_night_" + str(date) + ".tif", missouri_bounds, "QC_Night",True,91,32)
    prepare_files(modis_tiles,folder + "/missouri_qc_day_" + str(date) + ".tif", missouri_bounds, "QC_Day",True,91,32)"""
if __name__ == '__main__':
    prepare_files(["mod1.hdf","mod2.hdf"],"illinois.tif",illinois_bounds,"LST_Night_1km")
