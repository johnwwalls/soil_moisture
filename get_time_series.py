import tifffile
import os
from scipy import stats, optimize, interpolate
import matplotlib.pyplot as plt 
import numpy as np 
data_x = []
data_y = []
data_q = []
c = 0
for date in os.listdir("data"):
    try:
        img = tifffile.imread("data/" + date + "/illinois_" + date + ".tif")
        #for i in range(len(img)):
        #    for j in range(len(img[i])):
                #data_q.append(img[i][j][4])
                #data_q.append(img[i][j][5])
        #        if img[i][j][0] != 0 and .02*(img[i][j][2] - img[i][j][3]) < 10 and .02*(img[i][j][2] - img[i][j][3]) > -10 and img[i][j][4] > 15 and img[i][j][5] > 15:
        if c == 0:
            data_x = .02*(img[:,:,2] - img[:,:,3])
            print(np.average(data_x))
            data_y = img[:,:,0]
        else:
            data_x = data_x + np.abs(.02*(img[:,:,2] - img[:,:,3]))
            data_y = data_y + img[:,:,0]
                    #data_x.append(.02*(img[i][j][2] - img[i][j][3]))
                    #data_y.append(img[i][j][0])
        c = c + 1
    except:
        print("error")
print(data_x.shape)
print(data_y.shape)
print(np.average(data_x))
print((data_x/c)[:50,:40])
tifffile.imsave("x.tif",(data_x/c)[:50,:40] - 90)
tifffile.imsave("y.tif",data_y/c)
"""slope, intercept, r_value, p_value, std_err = stats.linregress(data_x, data_y)
print(np.average(np.array(data_q)))
print(slope)
print(intercept)
print(r_value**2)
print(len(data_x))
print(len(data_y))
plt.scatter(data_x, data_y)
plt.savefig('foo.png') """