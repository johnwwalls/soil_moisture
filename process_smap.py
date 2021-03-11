import numpy as np
import h5py
import matplotlib.pyplot as plt
illinois_bounds = (37.53114756912893,42.47492527271053,-91.8149898022461,-87.39462351501466)
oklahoma_bounds = (34.24527460247113,36.970101718281434,-102.9851672619629,-94.56955408752442)
def get_indices(lat_data,long_data,lat_min,lat_max,long_min,long_max):
    max_long = -1
    min_long = -1
    for long in range(len(long_data[0, :])):
        new = np.max(long_data[:, long])
        if new == -9999:
            continue
        if max_long == -1 and new > long_max:
            max_long = long
        if min_long == -1 and new > long_min:
            min_long = long

    max_lat = -1
    min_lat = -1
    for lat in range(len(lat_data[:, 0])):
        new = np.max(lat_data[lat, :])
        if new == -9999:
            continue
        if min_lat == -1 and new < lat_max:
            min_lat = lat
        if max_lat == -1 and new < lat_min:
            max_lat = lat

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

soil_moisture_am = get_soil_moisture_am("smap.h5",illinois_bounds)
soil_moisture_pm = get_soil_moisture_pm("smap.h5",illinois_bounds)

soil_moisture_am[soil_moisture_am == -9999] = 0
soil_moisture_pm[soil_moisture_pm == -9999] = 0

plt.figure()
_, arr = plt.subplots(3,1)
print(soil_moisture_am.shape)
arr[0].imshow(soil_moisture_am)
arr[1].imshow(soil_moisture_pm)
arr[2].imshow(soil_moisture_am - soil_moisture_pm)

print("sup")
