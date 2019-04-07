# Cory Press
# SWTools A08   
#   get_dominant_colors.py
#       
#       args-
#           image       - image to be made into a mosaic
#           folder      - folder that contains image you want to make your mosaic out of
#           pixels      - number of pixels the will be replaced by one image (closer to one the better)
#           size        - size of each sub image
#       output-
#           *image*_mosaic.png - creates a mosaic of image out of the images in folder
#
import cv2
import numpy as np
from PIL import Image, ImageDraw
import sys
import os
import requests
from math import sqrt
import json


#
#   getArgs
#       returns
#           dictionary of args
#
def getArgs():
    args = {}
    for arg in sys.argv[1:]:
        k,v = arg.split('=')
        args[k] = v
    return args


#
#   colorDistatnce
#       args
#           color1 - np.array of a rgb value
#           color2 - np.array of a rgb value
#       returns
#           float
#       function
#           calculates the Euclidean distance between to color
#
def colorDistatnce(c1, c2):
    return sqrt( ((c1[0]-c2[0])**2) +((c1[1]-c2[1])**2) + ((c1[2]-c2[2])**2) )



#main
args = getArgs()

jsonfile = "dominant_colors_" + args["folder"] + ".json"
pxl = int(args["pixels"])
size = int(args["size"])

#check that json of dominant has already been made
if os.path.isfile(jsonfile):
    f = open(jsonfile)
    dominant_colors = json.load(f)
else:
    print("json file of image not yet created") 

#open image
image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

w = image.shape[0]
h = image.shape[1]

#new image to draw on
newImg = Image.new('RGBA', (int(w/pxl)*size,int(h/pxl)*size), (255,255,255,255))
drawOnMe = ImageDraw.Draw(newImg)

#process through all pixel squares
for row in range(int(h/pxl)):
    for col in range(int(w/pxl)):
        #find average color
        avg = np.array([0.0, 0.0, 0.0])
        for i in range(pxl):
            for j in range(pxl):
                avg += image[row*pxl+i][col*pxl+j]
        avg /= (pxl**2)
        
        #find closest matching image
        closest_dist = sys.float_info.max
        closest = ""
        for name, color in dominant_colors.items():
            dist = colorDistatnce(avg, np.array(color))
            if dist < closest_dist:
                closest_dist = dist
                closest = name
        
        #paste image to mosaic
        im = Image.open("./" + args["folder"] + "/" + closest)
        im = im.resize((size, size))
        newImg.paste(im, (col*size, row*size))
    if  row%int(h/pxl/10) == 0:
        sys.stdout.write("=")
        sys.stdout.flush()

#paste new image over resize original
orig = Image.open(args["image"])
orig = orig.resize((int(w/pxl)*size,int(h/pxl)*size))
newImg = Image.alpha_composite(orig, newImg)

#save file
newfile = args["image"].split(".")
newImg.save(newfile[0] + "_mosaic." + newfile[1])


