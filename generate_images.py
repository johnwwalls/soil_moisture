import tifffile
import matplotlib.pyplot as plt
import numpy as np
import os

valid_land_cover_values = [14,18,19]

def get_good_land_cover(val):
    if val in valid_land_cover_values:
        return 1
    else:
        return 0
get_good_land_cover_vect = np.vectorize(get_good_land_cover)
def make_smap(state,date,outdir,pm):
    plt.clf()
    day_str = "am"
    if pm:
        day_str = "pm"
    if not os.path.exists(outdir + "/" + date):
        os.mkdir(outdir + "/" + date)
    imgog = tifffile.imread("data/" + date + "/" + state + "_land_cover_" + date + ".tif")
    img = imgog[:,:,0:1] #soil moisture am
    if pm:
        img = imgog[:,:,1:2] #soil moisture pm
    
    #img[img == -9999] = np.nan
    for i in range(len(imgog)):
        for j in range(len(imgog[i])):
            if not pm and not (imgog[i][j][0] != 0 and (imgog[i][j][2] == 0 or imgog[i][j][2] == 8) and (imgog[i][j][8] in valid_land_cover_values)):
                img[i,j] = np.nan
            elif pm and not (imgog[i][j][1] != 0 and (imgog[i][j][3] == 0 or imgog[i][j][3] == 8) and (imgog[i][j][8] in valid_land_cover_values)):
                img[i,j] = np.nan

    plt.title("Soil Moisture " + day_str + " in " + state + " for " + date)
    plot = plt.imshow(img[:,:,0])
    plt.colorbar(plot)
    plt.savefig(outdir + "/" + date + "/soil_moisture_" + day_str + "_" + state + "_" + date + ".png")
def make_lst(state,date,outdir,night):
    plt.clf()
    day_str = "day"
    if night:
        day_str = "night"
    if not os.path.exists(outdir + "/" + date):
        os.mkdir(outdir + "/" + date)
    imgog = tifffile.imread("data/" + date + "/" + state + "_land_cover_" + date + ".tif")
    img = imgog[:,:,4:5] * .02 #lst day
    if night:
        img = imgog[:,:,5:6] * .02 #lst night
    
    for i in range(len(imgog)):
        for j in range(len(imgog[i])):
            if not night and not (imgog[i][j][4] != 0 and imgog[i][j][6] > 0 and (imgog[i][j][8] in valid_land_cover_values)):
                img[i,j] = np.nan
            elif night and not (imgog[i][j][5] != 0 and imgog[i][j][7] > 0 and (imgog[i][j][8] in valid_land_cover_values)):
                img[i,j] = np.nan
                
    plt.title("LST " + day_str + " in " + state + " for " + date)
    plot = plt.imshow(img[:,:,0])
    plt.colorbar(plot)
    plt.savefig(outdir + "/" + date + "/lst_" + day_str + "_" + state + "_" + date + ".png")
def draw_date(date,outdir):
    make_smap("illinois",date,outdir, True)
    make_smap("illinois",date,outdir, False)
    make_lst("illinois",date,outdir, True)
    make_lst("illinois",date,outdir, False)

    make_smap("oklahoma",date,outdir, True)
    make_smap("oklahoma",date,outdir, False)
    make_lst("oklahoma",date,outdir, True)
    make_lst("oklahoma",date,outdir, False)

def get_all(outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for date in os.listdir("data"):
        print(date)
        draw_date(date,outdir)
#get_all("images")
draw_date("2019-08-24","images")