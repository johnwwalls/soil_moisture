import tifffile
import os
from scipy import stats, optimize, interpolate
import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.dates as mdates
import datetime as dt

def compare_sm_am(value):
    return value[0] > 0 and (value[2] == 0 or value[2] == 8)
def compare_sm_pm(value):
    return value[1] > 0 and (value[3] == 0 or value[3] == 8)
def compare_lst_day(value):
    return value[5] != 0 and value[7] != 0
def compare_lst_night(value):
    return value[4] != 0 and value[6] != 0
def compare(typ, val):
    if typ == "soil_moisture_am":
        return compare_sm_am(val)
    if typ == "soil_moisture_pm":
        return compare_sm_pm(val)
    if typ == "lst_day":
        return compare_lst_day(val)
    if typ == "lst_night":
        return compare_lst_night(val)
    return false

types = {
    "soil_moisture_am":0,
    "soil_moisture_pm":1,
    "lst_day":5,
    "lst_night":4,
}
def get_time_series(typ, state, i, j, scale):
    layer = types[typ]
    data_x = []
    data_y = []
    for date in sorted(os.listdir("data")):
        if True:
            img = tifffile.imread("data/" + date + "/" + state + "_" + date + ".tif")
            if len(img[i][j]) == 8 and compare(typ, img[i][j]):
                data_y.append(img[i][j][layer]*scale)
            else:
                data_y.append(np.nan)
            data_x.append(dt.datetime.strptime(date,'%Y-%m-%d').date())
        else:
            print("error")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))  
    plt.scatter(data_x, data_y)
    plt.title(typ + " " + state + " for i: " + str(i) + " and j: " + str(j))
    plt.gcf().autofmt_xdate()
    plt.savefig(typ + '_time_series/' + state + '_' + str(i) + '_' + str(j) + '.png') 
    plt.clf()
illinois_grids = [(10,20),(14,34),(19,32),(30,30),(31,41)]
oklahoma_grids = [(10,20),(11,41),(19,24),(19,35),(26,38)]

get_time_series('soil_moisture_am','illinois',27,40, .02)
get_time_series('soil_moisture_pm','illinois',27,40, .02)
for grid in illinois_grids:
    """get_time_series('soil_moisture_am','illinois',grid[0],grid[1], 1)
    get_time_series('soil_moisture_pm','illinois',grid[0],grid[1], 1)
    get_time_series('lst_day','illinois',grid[0],grid[1], .02)"""
    get_time_series('lst_night','illinois',grid[0],grid[1], .02)
"""for grid in oklahoma_grids:
    get_time_series('soil_moisture_am','oklahoma',grid[0],grid[1], 1)
    get_time_series('soil_moisture_pm','oklahoma',grid[0],grid[1], 1)
    get_time_series('lst_day','oklahoma',grid[0],grid[1], .02)
    get_time_series('lst_night','oklahoma',grid[0],grid[1], .02)"""