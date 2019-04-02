import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter


#   compareImages
#
#       given to images gives returns the Mean Square error 
#       between the two.
#
def compareImages(imageFile1, imageFile2):
    im1 = Image.open(imageFile1)
    im1 = im1.convert('RGB')
    imlist1 = list(im1.getdata())
    w,h = im1.size

    im2 = Image.open(imageFile2)
    im2 = im2.convert('RGB')
    im2 = im2.resize((w,h))
    imlist2 = list(im2.getdata())

    w,h = im1.size

    sum = 0.0
    for i in range(len(imlist1)):
        for j in range(len(imlist1[i])):
            sum += ((imlist1[i][j] - imlist2[i][j]) ** 2)
       

    return sum/(w*h)

#retrieve args - from dr. griffin
args = {}
for arg in sys.argv[1:]:
    k,v = arg.split('=')
    args[k] = v

#loop through all images and compare them to original while
#keeping track of the closest
low = 1000000000
closestImage = ""
for image in os.listdir(args["folder"]):
    if image != args["image"]:
        mse = compareImages("./" + args["folder"] + "/" + image, "./" + args["folder"] + "/" + args["image"])
        if mse < low:
            closestImage = image
            low = mse


#create new image to show origanl and closest and display it
im1 = Image.open("./" + args["folder"] + "/" + args["image"])
w,h = im1.size
im2 = Image.open("./" + args["folder"] + "/" + closestImage)
im2 = im2.resize((w,h))


newImg = Image.new('RGBA', (w*2+100, h+100), (255,255,255,255))

drawOnMe = ImageDraw.Draw(newImg)

fnt = ImageFont.truetype("arial.ttf", 12)

drawOnMe.text((10,10), "original\n"+args["image"], font=fnt, fill=(0,0,0,255))
drawOnMe.text((60+w,10), "closest\n"+closestImage, font=fnt, fill=(0,0,0,255))

newImg.paste(im1, (10, 50))
newImg.paste(im2, (60+w, 50))

newImg.show()
