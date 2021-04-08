import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tifffile
import os
from scipy import stats, optimize, interpolate
import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.dates as mdates
import datetime as dt

fig,ax = plt.subplots(figsize=(20,10))

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
def get_time_series(typ, state, i1,i2, j1,j2, scale):
    layer = types[typ]
    data_x = []
    data_y = []
    for date in sorted(os.listdir("data")):
        if True:
            img = tifffile.imread("data/" + date + "/" + state + "_" + date + ".tif")
            y = 0
            c = 0
            for i in range(i1,i2):
                for j in range(j1,j2):
                    if len(img[i][j]) == 8 and compare(typ, img[i][j]):
                        #data_y.append(img[i][j][layer]*scale)
                        c = c + 1
                        y = y + img[i][j][layer]*scale
                    else:
                        #data_y.append(np.nan)
                        c = c
            if c > 0:
                y = y / c
                data_y.append(y)
                data_x.append(dt.datetime.strptime(date,'%Y-%m-%d').date())
            else:
                data_y.append(np.nan)
                data_x.append(dt.datetime.strptime(date,'%Y-%m-%d').date())
        else:
            print("error")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))  
    ax.scatter(data_x, data_y)
    plt.gcf().autofmt_xdate()
   
get_time_series('soil_moisture_am','illinois',23,27,37,41, 1)

values = []
dates = []
with open('cmiday.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='	', quotechar='|')
    for row in spamreader:
        try:
            if row[0] != "" and int(row[0]) == 2019 and row[1] != "" and int(row[1]) >= 8:
                values.append(float(row[25]))
                dates.append(datetime.datetime(int(row[0]),int(row[1]),int(row[2])))
            elif row[0] != "" and int(row[0]) == 2020:
                values.append(float(row[25]))
                dates.append(datetime.datetime(int(row[0]),int(row[1]),int(row[2])))
        except:
            print("error")
with open('cmiday21.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='	', quotechar='|')
    for row in spamreader:
        try:
            if row[1] != "" and int(row[2]) <= 19:
                values.append(float(row[25]))
                dates.append(datetime.datetime(int(row[0]),int(row[1]),int(row[2])))
        except:
            print("error")
ax2=ax.twinx()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))  
ax2.bar(dates, values)
plt.title("precipitation for champaign")
plt.gcf().autofmt_xdate()
fig.savefig("precipitation_champaign.png") 
plt.clf()
        