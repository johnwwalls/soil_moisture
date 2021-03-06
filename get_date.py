import process_smap
import process_modis
import download_smap
import download_modis
import os
import netrc

def get_date_smap(date, folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    files = download_smap.main(date)
    smap_file = ""
    for fil in files:
        if fil[-3:] == '.h5':
            smap_file = fil
    if smap_file == "":
        raise Exception("The downloaded smap h5 file wasn't found.")
    process_smap.get_soil_moisture(smap_file, date, folder)
    for fil in files:
        os.remove(fil)
def get_date_modis(date, folder):
    command = "rm -rf modistemp"
    os.system(command)
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.mkdir("modistemp")
    download_modis.download_date(date, "modistemp")
    modis_tiles = []
    for fil in os.listdir("modistemp"):
        if fil[-4:] == '.hdf':
            modis_tiles.append("modistemp/" + fil)
    process_modis.get_soil_temperature(date, modis_tiles, folder)
    command = "rm -rf modistemp"
    os.system(command)
def get_date_mydis(date, folder):
    command = "rm -rf mydistemp"
    os.system(command)
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.mkdir("mydistemp")
    download_modis.download_date_myd(date, "mydistemp")
    modis_tiles = []
    for fil in os.listdir("mydistemp"):
        if fil[-4:] == '.hdf':
            modis_tiles.append("mydistemp/" + fil)
    process_modis.get_soil_temperature(date, modis_tiles, folder)
    command = "rm -rf mydistemp"
    os.system(command)
def merge(inps,outp):
    command = "gdal_merge.py -o " + outp + " -separate "
    for inp in inps:
        command = command + inp + " "
    os.system(command)
def get_date(date, modis_dir, smap_dir,out_dir,mydis_dir):
    get_date_modis(date,modis_dir)
    #get_date_mydis(date,mydis_dir)
    get_date_smap(date,smap_dir)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    merge([smap_dir + "/soil_moisture_am_illinois_" + str(date) + ".tif",smap_dir + "/soil_moisture_pm_illinois_" + str(date) + ".tif",smap_dir + "/qc_am_illinois_" + str(date) + ".tif",smap_dir + "/qc_pm_illinois_" + str(date) + ".tif",modis_dir + "/illinois_lst_day_" + str(date) + ".tif",modis_dir + "/illinois_lst_night_" + str(date) + ".tif",modis_dir + "/illinois_qc_night_" + str(date) + ".tif",modis_dir + "/illinois_qc_day_" + str(date) + ".tif"],out_dir + "/illinois_" + str(date) + ".tif")
    merge([smap_dir + "/soil_moisture_am_oklahoma_" + str(date) + ".tif",smap_dir + "/soil_moisture_pm_oklahoma_" + str(date) + ".tif",smap_dir + "/qc_am_oklahoma_" + str(date) + ".tif",smap_dir + "/qc_pm_oklahoma_" + str(date) + ".tif",modis_dir + "/oklahoma_lst_day_" + str(date) + ".tif",modis_dir + "/oklahoma_lst_night_" + str(date) + ".tif",modis_dir + "/oklahoma_qc_night_" + str(date) + ".tif",modis_dir + "/oklahoma_qc_day_" + str(date) + ".tif"],out_dir + "/oklahoma_" + str(date) + ".tif")
    
    #merge([smap_dir + "/soil_moisture_am_illinois_" + str(date) + ".tif",smap_dir + "/soil_moisture_pm_illinois_" + str(date) + ".tif",smap_dir + "/qc_am_illinois_" + str(date) + ".tif",smap_dir + "/qc_pm_illinois_" + str(date) + ".tif",modis_dir + "/illinois_lst_day_" + str(date) + ".tif",modis_dir + "/illinois_lst_night_" + str(date) + ".tif",modis_dir + "/illinois_qc_night_" + str(date) + ".tif",modis_dir + "/illinois_qc_day_" + str(date) + ".tif",mydis_dir + "/illinois_lst_day_" + str(date) + ".tif",mydis_dir + "/illinois_lst_night_" + str(date) + ".tif",mydis_dir + "/illinois_qc_night_" + str(date) + ".tif",mydis_dir + "/illinois_qc_day_" + str(date) + ".tif"],out_dir + "/illinois_" + str(date) + ".tif")
    #merge([smap_dir + "/soil_moisture_am_oklahoma_" + str(date) + ".tif",smap_dir + "/soil_moisture_pm_oklahoma_" + str(date) + ".tif",smap_dir + "/qc_am_oklahoma_" + str(date) + ".tif",smap_dir + "/qc_pm_oklahoma_" + str(date) + ".tif",modis_dir + "/oklahoma_lst_day_" + str(date) + ".tif",modis_dir + "/oklahoma_lst_night_" + str(date) + ".tif",modis_dir + "/oklahoma_qc_night_" + str(date) + ".tif",modis_dir + "/oklahoma_qc_day_" + str(date) + ".tif",mydis_dir + "/oklahoma_lst_day_" + str(date) + ".tif",mydis_dir + "/oklahoma_lst_night_" + str(date) + ".tif",mydis_dir + "/oklahoma_qc_night_" + str(date) + ".tif",mydis_dir + "/oklahoma_qc_day_" + str(date) + ".tif"],out_dir + "/oklahoma_" + str(date) + ".tif")
    #merge([smap_dir + "/soil_moisture_am_missouri_" + str(date) + ".tif",smap_dir + "/soil_moisture_pm_missouri_" + str(date) + ".tif",smap_dir + "/qc_am_missouri_" + str(date) + ".tif",smap_dir + "/qc_pm_missouri_" + str(date) + ".tif",modis_dir + "/missouri_lst_day_" + str(date) + ".tif",modis_dir + "/missouri_lst_night_" + str(date) + ".tif",modis_dir + "/missouri_qc_night_" + str(date) + ".tif",modis_dir + "/missouri_qc_day_" + str(date) + ".tif"],out_dir + "/missouri_" + str(date) + ".tif")

from datetime import date, timedelta


def get_all():
    sdate = date(2019, 8, 1)   # start date
    edate = date(2020, 3, 3)   # end date

    delta = edate - sdate       # as timedelta

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        print(day)
        get_date(day,"modis_data/" + str(day),"smap_data/" + str(day),"data/" + str(day),"mydis_data/" + str(day))

get_all()
#day = "2018-08-13"
#get_date(day,"modis_data/" + str(day),"smap_data/" + str(day),"data/" + str(day),"mydis_data/" + str(day))
