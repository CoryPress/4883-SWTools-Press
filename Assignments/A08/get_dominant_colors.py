# Cory Press
# SWTools A08   
#   get_dominant_colors.py
#       
#       args-
#           imagefolder - folder that contains image you want to make your mosaic out of
#           n           - number of clusters
#       output-
#           dominant_colors_*imagefloder*.json - maps all images in image folder to their most
#               dominant color
#
import cv2
import numpy as np
from PIL import Image
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
#   getDominant
#       args
#           img - image file
#           n - number of dominant colors
#       returns
#           using kmeans creates a list of n dominant colors
#
def getDominant(img, n):

    # open image and format properly to be able create cluster
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape(image.shape[0]*image.shape[1], 3)
    image = np.float32(image)


    flags = cv2.KMEANS_RANDOM_CENTERS
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    _, labels, palette = cv2.kmeans(image, n, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]

    #convert color to list so it can be saved in json
    dominant = dominant.tolist()
    return dominant


#main
args = getArgs()

dominant_colors = {}

#find dominant colors of all images
for image in os.listdir(".\\" + args["folder"]):
    dominant_colors[image] = getDominant(".\\" + args["folder"] + "\\" + image, int(args["n"]))

#save as json so you it can be used to create multiple mosaics
f = open("dominant_colors_" + args["folder"] + ".json","w")
f.write(json.dumps(dominant_colors))
f.close()







