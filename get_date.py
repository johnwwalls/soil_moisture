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
def get_date(date, modis_dir, smap_dir):
    get_date_modis(date,modis_dir)
    get_date_smap(date,smap_dir)
get_date("2020-03-03","modis_data","smap_data")

