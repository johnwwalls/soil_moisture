import tifffile
import os
from scipy import stats, optimize, interpolate
import matplotlib.pyplot as plt 
import numpy as np 

valid_land_cover_values = [14,18,19]

def get_regression_map(state, typ):
    data_x1 = []
    data_x2 = []
    data_xdiff = []
    data_y = []
    count = 0
    for date in os.listdir("data"):
        month = int(date[5:7])
        if month < 8 and month >= 0:
            continue
        if True:
            img = tifffile.imread("data/" + date + "/" + state + "_land_cover_" + date + ".tif")
            for i in range(0,len(img)):
                if count == 0:
                    data_x1.append([])
                    data_x2.append([])
                    data_xdiff.append([])
                    data_y.append([])
                for j in range(len(img[i])):
                    if count == 0:
                        data_x1[i].append([])
                        data_x2[i].append([])
                        data_xdiff[i].append([])
                        data_y[i].append([])
                    if len(img[i][j]) < 9:
                        continue
                    if typ == "am":
                        if img[i][j][4] != 0 and img[i][j][5] != 0 and img[i][j][6] < 64 and img[i][j][7] < 64 and img[i][j][0] > 0 and (img[i][j][2] == 0 or img[i][j][2] == 8) and (img[i][j][8] in valid_land_cover_values):
                            data_x1[i][j].append(img[i][j][4]*.02)
                            data_x2[i][j].append(img[i][j][5]*.02)
                            data_xdiff[i][j].append(img[i][j][4]*.02 - img[i][j][5]*.02)
                            data_y[i][j].append(img[i][j][0])
                    if typ == "pm":
                        if img[i][j][4] != 0 and img[i][j][5] != 0 and img[i][j][6] < 64 and img[i][j][7] < 64 and img[i][j][1] > 0 and (img[i][j][3] == 0 or img[i][j][3] == 8) and (img[i][j][8] in valid_land_cover_values):
                            data_x1[i][j].append(img[i][j][4]*.02)
                            data_x2[i][j].append(img[i][j][5]*.02)
                            data_xdiff[i][j].append(img[i][j][4]*.02 - img[i][j][5]*.02)
                            data_y[i][j].append(img[i][j][1])
            count = count + 1
        else:
            print("error")

    r_2 = []
    l = []
    for i in range(len(data_x1)):
        r_2.append([])
        l.append([])
        for j in range(len(data_x1[i])):
            if len(data_xdiff[i][j]) != 0:
                slope, intercept, r_value, p_value, std_err = stats.linregress(data_xdiff[i][j], data_y[i][j])
                r_2[i].append(r_value**2)
            else:
                r_2[i].append(0)
            l[i].append(len(data_xdiff[i][j]))
    
    r_2 = np.asarray(r_2)
    l = np.asarray(l)
    plot = plt.imshow(r_2)

    plt.title('regression by grid ' + state + ' ' + typ)
    plt.colorbar(plot)
    plt.savefig('regression_by_grid_land_cover/' + state + '_' + typ + '.png') 
    plt.clf()

    plot2 = plt.imshow(l)

    plt.title('regression length by grid ' + state + ' ' + typ)
    plt.colorbar(plot2)
    plt.savefig('regression_by_grid_land_cover/' + state + '_length_' + typ + '.png') 
    plt.clf()

get_regression_map("illinois","am")
get_regression_map("illinois","pm")
get_regression_map("oklahoma","am")
get_regression_map("oklahoma","pm")
#get_regression_map("missouri","am")
#get_regression_map("missouri","pm")
