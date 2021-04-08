import tifffile
import os
from scipy import stats, optimize, interpolate
import matplotlib.pyplot as plt 
import numpy as np 

valid_land_cover_values = [14,18,19]

def get_regression_super(state, typ):
    data_x1 = []
    data_x2 = []
    data_xdiff = []
    data_y = []
    i = 0
    for date in os.listdir("data"):
        month = int(date[5:7])
        if month < 8 and month >= 0:
            continue
        if True:
            img = tifffile.imread("data/" + date + "/" + state + "_land_cover_2_" + date + ".tif")
            x1 = 0
            x2 = 0
            y = 0
            c = 0
            i = i +1
            for i in range(0,len(img)):
                for j in range(len(img[i])):
                    if len(img[i][j]) < 9:
                        continue
                    if typ == "am":
                        if img[i][j][4] != 0 and img[i][j][5] != 0 and img[i][j][6] != 0 and img[i][j][7] != 0 and img[i][j][0] > 0 and (img[i][j][2] == 0 or img[i][j][2] == 8) and (img[i][j][8] in valid_land_cover_values):
                            x1 = x1 + img[i][j][4]
                            x2 = x2 + img[i][j][5]
                            y = y + img[i][j][0]
                            c = c + 1
                    if typ == "pm":
                        if img[i][j][4] != 0 and img[i][j][5] != 0 and img[i][j][6] != 0 and img[i][j][7] != 0 and img[i][j][1] > 0 and (img[i][j][3] == 0 or img[i][j][3] == 8) and (img[i][j][8] in valid_land_cover_values):
                            x1 = x1 + img[i][j][4]
                            x2 = x2 + img[i][j][5]
                            y = y + img[i][j][1]
                            c = c + 1
            if c != 0:
                x1 = x1 / c
                x2 = x2 / c
                y = y / c 
                x1 = x1 * .02
                x2 = x2 * .02
                data_x1.append(x1)
                data_x2.append(x2)
                data_y.append(y)
                data_xdiff.append(x1 - x2)
        else:
            print("error")
    print(len(data_x1))
    print(len(data_x2))
    print(len(data_xdiff))
    print(len(data_y))

    slope, intercept, r_value, p_value, std_err = stats.linregress(data_xdiff, data_y)

    print(slope)
    print(intercept)
    print(r_value**2)

    plt.scatter(data_xdiff, data_y)

    x = np.linspace(-20,40,100)
    y = slope*x+intercept
    plt.plot(x, y, '-r', label=r_value**2)
    plt.title('regression super ' + state + ' ' + typ)
    plt.savefig('regression_super_land_cover/' + state + '_' + typ + '.png') 
    plt.clf()
def get_regression(state, typ):
    data_x1 = []
    data_x2 = []
    data_xdiff = []
    data_y = []
    i = 0
    for date in os.listdir("data"):
        month = int(date[5:7])
        if month < 8 and month >= 0:
            continue
        if True:
            img = tifffile.imread("data/" + date + "/" + state + "_land_cover_" + date + ".tif")
            for i in range(0,len(img)):
                for j in range(len(img[i])):
                    if len(img[i][j]) < 9:
                        continue
                    if typ == "am":
                        if img[i][j][4] != 0 and img[i][j][5] != 0 and img[i][j][6] != 0 and img[i][j][7] != 0 and img[i][j][0] > 0 and (img[i][j][2] == 0 or img[i][j][2] == 8) and (img[i][j][8] in valid_land_cover_values):
                            data_x1.append(img[i][j][4]*.02)
                            data_x2.append(img[i][j][5]*.02)
                            data_xdiff.append(img[i][j][4]*.02 - img[i][j][5]*.02)
                            data_y.append(img[i][j][0])
                    if typ == "pm":
                        if img[i][j][4] != 0 and img[i][j][5] != 0 and img[i][j][6] != 0 and img[i][j][7] != 0 and img[i][j][1] > 0 and (img[i][j][3] == 0 or img[i][j][3] == 8) and (img[i][j][8] in valid_land_cover_values):
                            data_x1.append(img[i][j][4]*.02)
                            data_x2.append(img[i][j][5]*.02)
                            data_xdiff.append(img[i][j][4]*.02 - img[i][j][5]*.02)
                            data_y.append(img[i][j][1])
        else:
            print("error")
    print(len(data_x1))
    print(len(data_x2))
    print(len(data_xdiff))
    print(len(data_y))

    slope, intercept, r_value, p_value, std_err = stats.linregress(data_xdiff, data_y)

    print(slope)
    print(intercept)
    print(r_value**2)

    plt.scatter(data_xdiff, data_y)

    x = np.linspace(-20,40,100)
    y = slope*x+intercept
    plt.plot(x, y, '-r', label=r_value**2)
    plt.title('regression ' + state + ' ' + typ)
    plt.savefig('regression_land_cover/' + state + '_' + typ + '.png') 
    plt.clf()

get_regression("illinois","am")
get_regression("illinois","pm")
get_regression("oklahoma","am")
get_regression("oklahoma","pm")

get_regression_super("illinois","am")
get_regression_super("illinois","pm")
get_regression_super("oklahoma","am")
get_regression_super("oklahoma","pm")
