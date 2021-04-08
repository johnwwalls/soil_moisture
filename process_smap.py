import numpy as np
import h5py
import matplotlib.pyplot as plt
import tifffile
import os
import gdal
import osr
illinois_bounds = (37.53114756912893,42.47492527271053,-91.8149898022461,-87.39462351501466)
oklahoma_bounds = (34.24527460247113,36.970101718281434,-102.9851672619629,-94.56955408752442)

def add_geo_transform(inp,outp,lat_min,lat_max,long_min,long_max):
    np_data = tifffile.imread(inp)
    num_cols = float(np_data.shape[1])
    num_rows = float(np_data.shape[0])

    xmin = long_min
    xmax = long_max
    ymin = lat_min
    ymax = lat_max
    xres = (xmax - xmin) / num_cols
    yres = (ymax - ymin) / num_rows

    nrows, ncols = np_data.shape
    xres = (xmax - xmin) / float(ncols)
    yres = (ymax - ymin) / float(nrows)
    geotransform = (xmin, xres, 0, ymax, 0, -xres)

    dataFileOutput = outp
    output_raster = gdal.GetDriverByName('GTiff').Create(dataFileOutput, ncols, nrows, 1, gdal.GDT_Float32) # Open the file
    output_raster.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    output_raster.SetProjection(srs.ExportToWkt())
    output_raster.GetRasterBand(1).WriteArray(np_data) # Writes my array to the raster

    del output_raster
def get_indices(lat_data,long_data,lat_min,lat_max,long_min,long_max):
    max_long_ind = -1
    min_long_ind = -1
    max_long = -1
    min_long = -1
    for long in range(len(long_data[0, :])):
        new = np.max(long_data[:, long])
        if new == -9999:
            continue
        if max_long == -1 and new > long_max:
            max_long_ind = long
            max_long = new
        if min_long == -1 and new > long_min:
            min_long_ind = long
            min_long = new

    max_lat_ind = -1
    min_lat_ind = -1
    max_lat = -1
    min_lat = -1
    for lat in range(len(lat_data[:, 0])):
        new = np.max(lat_data[lat, :])
        if new == -9999:
            continue
        if min_lat == -1 and new < lat_max:
            min_lat_ind = lat
            min_lat = new
        if max_lat == -1 and new < lat_min:
            max_lat_ind = lat
            max_lat = new
    #max_lat and min_lat should be swapper because the order of the indexes is opposite
    return min_lat_ind,max_lat_ind,min_long_ind,max_long_ind,max_lat,min_lat,min_long,max_long
def get_soil_moisture_am(file_name, bounds):
    lat_min,lat_max,long_min,long_max = bounds

    main_file = h5py.File(file_name, 'r')

    group_id=list(main_file.keys())[1];# < Lets focus on the AM overpass for this example

    soil_moisture_id = list(main_file[group_id].keys())[24] #soil moisture
    qc_id = list(main_file[group_id].keys())[16] #qc

    soil_moisture_data = main_file[group_id][soil_moisture_id][:,:]
    qc_data = main_file[group_id][qc_id][:,:]

    lat_id = list(main_file[group_id].keys())[11]
    long_id = list(main_file[group_id].keys())[13]

    lat_data = main_file[group_id][lat_id][:,:]
    long_data = main_file[group_id][long_id][:,:]

    min_lat_ind, max_lat_ind, min_long_ind, max_long_ind, min_lat, max_lat, min_long, max_long = get_indices(lat_data,long_data,lat_min,lat_max,long_min,long_max)

    return soil_moisture_data[min_lat_ind:max_lat_ind, min_long_ind:max_long_ind], qc_data[min_lat_ind:max_lat_ind, min_long_ind:max_long_ind], min_lat, max_lat, min_long, max_long


def get_soil_moisture_pm(file_name, bounds):
    lat_min, lat_max, long_min, long_max = bounds

    main_file = h5py.File(file_name, 'r')

    group_id = list(main_file.keys())[2];  # < Lets focus on the AM overpass for this example
    
    soil_moisture_id = list(main_file[group_id].keys())[26] #soil moisture pm
    qc_id = list(main_file[group_id].keys())[17] #qc pm

    soil_moisture_data = main_file[group_id][soil_moisture_id][:, :]
    qc_data = main_file[group_id][qc_id][:, :]

    lat_id = list(main_file[group_id].keys())[12]
    long_id = list(main_file[group_id].keys())[14]

    lat_data = main_file[group_id][lat_id][:, :]
    long_data = main_file[group_id][long_id][:, :]

    min_lat_ind, max_lat_ind, min_long_ind, max_long_ind, min_lat, max_lat, min_long, max_long = get_indices(lat_data,long_data,lat_min,lat_max,long_min,long_max)

    return soil_moisture_data[min_lat_ind:max_lat_ind, min_long_ind:max_long_ind],qc_data[min_lat_ind:max_lat_ind, min_long_ind:max_long_ind], min_lat, max_lat, min_long, max_long
def get_soil_moisture(smap_file, date, folder):
    soil_moisture_am_illinois,qc_am_illinois,min_lat,max_lat,min_long,max_long = get_soil_moisture_am(smap_file,illinois_bounds)
    tifffile.imsave(folder + "/soil_moisture_am_illinois_" + str(date) + "temp.tif",soil_moisture_am_illinois)
    add_geo_transform(folder + "/soil_moisture_am_illinois_" + str(date) + "temp.tif",folder + "/soil_moisture_am_illinois_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/soil_moisture_am_illinois_" + str(date) + "temp.tif")
    tifffile.imsave(folder + "/qc_am_illinois_" + str(date) + "temp.tif",qc_am_illinois)
    add_geo_transform(folder + "/qc_am_illinois_" + str(date) + "temp.tif",folder + "/qc_am_illinois_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/qc_am_illinois_" + str(date) + "temp.tif")

    soil_moisture_pm_illinois,qc_pm_illinois,min_lat,max_lat,min_long,max_long = get_soil_moisture_pm(smap_file,illinois_bounds)
    tifffile.imsave(folder + "/soil_moisture_pm_illinois_" + str(date) + "temp.tif",soil_moisture_pm_illinois)
    add_geo_transform(folder + "/soil_moisture_pm_illinois_" + str(date) + "temp.tif",folder + "/soil_moisture_pm_illinois_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/soil_moisture_pm_illinois_" + str(date) + "temp.tif")
    tifffile.imsave(folder + "/qc_pm_illinois_" + str(date) + "temp.tif",qc_pm_illinois)
    add_geo_transform(folder + "/qc_pm_illinois_" + str(date) + "temp.tif",folder + "/qc_pm_illinois_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/qc_pm_illinois_" + str(date) + "temp.tif")

    soil_moisture_am_oklahoma,qc_am_oklahoma,min_lat,max_lat,min_long,max_long = get_soil_moisture_am(smap_file,oklahoma_bounds)
    tifffile.imsave(folder + "/soil_moisture_am_oklahoma_" + str(date) + "temp.tif",soil_moisture_am_oklahoma)
    add_geo_transform(folder + "/soil_moisture_am_oklahoma_" + str(date) + "temp.tif",folder + "/soil_moisture_am_oklahoma_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/soil_moisture_am_oklahoma_" + str(date) + "temp.tif")
    tifffile.imsave(folder + "/qc_am_oklahoma_" + str(date) + "temp.tif",qc_am_oklahoma)
    add_geo_transform(folder + "/qc_am_oklahoma_" + str(date) + "temp.tif",folder + "/qc_am_oklahoma_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/qc_am_oklahoma_" + str(date) + "temp.tif")

    soil_moisture_pm_oklahoma, qc_pm_oklahoma,min_lat,max_lat,min_long,max_long = get_soil_moisture_pm(smap_file,oklahoma_bounds)
    tifffile.imsave(folder + "/soil_moisture_pm_oklahoma_" + str(date) + "temp.tif",soil_moisture_pm_oklahoma)
    add_geo_transform(folder + "/soil_moisture_pm_oklahoma_" + str(date) + "temp.tif",folder + "/soil_moisture_pm_oklahoma_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/soil_moisture_pm_oklahoma_" + str(date) + "temp.tif")
    tifffile.imsave(folder + "/qc_pm_oklahoma_" + str(date) + "temp.tif",qc_pm_oklahoma)
    add_geo_transform(folder + "/qc_pm_oklahoma_" + str(date) + "temp.tif",folder + "/qc_pm_oklahoma_" + str(date) + ".tif",min_lat,max_lat,min_long,max_long)
    os.remove(folder + "/qc_pm_oklahoma_" + str(date) + "temp.tif")

if __name__ == '__main__':
    soil_moisture_am = get_soil_moisture_am("SMAP_L3_SM_P_E_20200303_R17000_001.h5",illinois_bounds)
    soil_moisture_pm = get_soil_moisture_pm("SMAP_L3_SM_P_E_20200303_R17000_001.h5",illinois_bounds)

    soil_moisture_am[soil_moisture_am == -9999] = 0
    soil_moisture_pm[soil_moisture_pm == -9999] = 0

    plt.figure()
    _, arr = plt.subplots(3,1)
    print(soil_moisture_am.shape)
    arr[0].imshow(soil_moisture_am)
    arr[1].imshow(soil_moisture_pm)
    arr[2].imshow(soil_moisture_am - soil_moisture_pm)

    print("sup")

"""import numpy as np
import h5py
import matplotlib.pyplot as plt
import tifffile
illinois_bounds = (37.53114756912893,42.47492527271053,-91.8149898022461,-87.39462351501466)
oklahoma_bounds = (34.24527460247113,36.970101718281434,-102.9851672619629,-94.56955408752442)
def get_indices(lat_data,long_data,lat_min,lat_max,long_min,long_max):
    max_long = -1
    min_long = -1
    for longl in range(len(long_data[0, :])):
        new = np.max(long_data[:, longl])
        try:
            if new == -9999:
                continue
            if max_long == -1 and new > long_max:
                max_long = longl
                print("max long " + str(new))
            if min_long == -1 and new > long_min:
                min_long = longl
                print("min long " + str(new))
        except:
            print(longl)
            print(new)
            print(long_min)
            print(long_max)

    max_lat = -1
    min_lat = -1
    for lat in range(len(lat_data[:, 0])):
        new = np.max(lat_data[lat, :])
        try:
            if new == -9999:
                continue
            if min_lat == -1 and new < lat_max:
                min_lat = lat
                print("max lat " + str(new))
            if max_lat == -1 and new < lat_min:
                max_lat = lat_data
                print("min lat " + str(new))
        except:
            print(lat)
            print(new)
            print(lat_min)
            print(lat_max)
    return min_lat,max_lat,min_long,max_long
def get_soil_moisture_am(file_name, bounds):
    lat_min,lat_max,long_min,long_max = bounds

    main_file = h5py.File(file_name, 'r')

    group_id=list(main_file.keys())[1];# < Lets focus on the AM overpass for this example

    soil_moisture_id = list(main_file[group_id].keys())[24]

    soil_moisture_data = main_file[group_id][soil_moisture_id][:,:]

    lat_id = list(main_file[group_id].keys())[11]
    long_id = list(main_file[group_id].keys())[13]

    lat_data = main_file[group_id][lat_id][:,:]
    long_data = main_file[group_id][long_id][:,:]

    min_lat, max_lat, min_long, max_long = get_indices(lat_data,long_data,lat_min,lat_max,long_min,long_max)

    return soil_moisture_data[min_lat:max_lat, min_long:max_long]


def get_soil_moisture_pm(file_name, bounds):
    lat_min, lat_max, long_min, long_max = bounds

    main_file = h5py.File(file_name, 'r')

    group_id = list(main_file.keys())[2];  # < Lets focus on the AM overpass for this example

    soil_moisture_id = list(main_file[group_id].keys())[26]

    soil_moisture_data = main_file[group_id][soil_moisture_id][:, :]

    lat_id = list(main_file[group_id].keys())[12]
    long_id = list(main_file[group_id].keys())[14]

    lat_data = main_file[group_id][lat_id][:, :]
    long_data = main_file[group_id][long_id][:, :]

    min_lat, max_lat, min_long, max_long = get_indices(lat_data, long_data, lat_min, lat_max, long_min, long_max)

    return soil_moisture_data[min_lat:max_lat, min_long:max_long]

def get_soil_moisture(smap_file, date, folder):
    soil_moisture_am_illinois = get_soil_moisture_am(smap_file,illinois_bounds)
    soil_moisture_pm_illinois = get_soil_moisture_pm(smap_file,illinois_bounds)
    soil_moisture_am_oklahoma = get_soil_moisture_am(smap_file,oklahoma_bounds)
    soil_moisture_pm_oklahoma = get_soil_moisture_pm(smap_file,oklahoma_bounds)

    tifffile.imsave(folder + "/soil_moisture_am_illinois_" + str(date) + ".tif",soil_moisture_am_illinois)
    tifffile.imsave(folder + "/soil_moisture_pm_illinois_" + str(date) + ".tif",soil_moisture_pm_illinois)
    tifffile.imsave(folder + "/soil_moisture_am_oklahoma_" + str(date) + ".tif",soil_moisture_am_oklahoma)
    tifffile.imsave(folder + "/soil_moisture_pm_oklahoma_" + str(date) + ".tif",soil_moisture_pm_oklahoma)
if __name__ == '__main__':
    soil_moisture_am = get_soil_moisture_am("test.h5",illinois_bounds)
    soil_moisture_pm = get_soil_moisture_pm("test.h5",illinois_bounds)

    soil_moisture_am[soil_moisture_am == -9999] = 0
    soil_moisture_pm[soil_moisture_pm == -9999] = 0
    tifffile.imsave("test2.tif",soil_moisture_am)
    plt.figure()
    _, arr = plt.subplots(3,1)
    print(soil_moisture_am.shape)
    arr[0].imshow(soil_moisture_am)
    arr[1].imshow(soil_moisture_pm)
    arr[2].imshow(soil_moisture_am - soil_moisture_pm)

    print("sup")"""
