import tifffile

img = tifffile.imread("land_cover.tif")
vals = {}
for i in range(len(img)):
    for j in range(len(img[i])):
        if img[i][j] not in vals.keys():
            vals[img[i][j]] = " " 
            print(str(img[i][j]) + " " + str(i) + " " + str(j))

#9-82, 6,11-81, 