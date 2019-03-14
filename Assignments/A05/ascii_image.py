#Cory Press
#A05
#Given an image path, name of new image, font to use, and font size to use
#   creates a new image out of the given image and recreates a greyscaled 
#   version using character from the font

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter


#given the path to an image and a font
#   creates a new image out of ascii that resembles a grey-scaled version
#   of the original
def convertToASCII(originF, fnt):

    #open image and convert to grayscale
    im = Image.open(originF)
    
    imlist = list(im.getdata())

    #greyscale
    #im = im.convert("L")

    w,h = im.size
    
    ascii_chars = [ 'y', 'd', 'c', '6', 'W', 'p', 'm', 'q', 'w', 'n', 'N']

    newImg = Image.new('RGBA', (w*fnt.size, h*fnt.size), (255,255,255,255))

    
    drawOnMe = ImageDraw.Draw(newImg)

    x = 0
    y = 0
    for pixel in imlist:
        avg = int((pixel[0]+pixel[1]+pixel[2])/3)
        ch = ascii_chars[avg // 25]
        drawOnMe.text((x,y), ch, font=fnt, fill=(pixel[0],pixel[1],pixel[2],255))
        x += fnt.size
        if x >= newImg.size[0]:
            x = 0
            y += fnt.size
    

    return newImg



originFile = "input_images/" + sys.argv[1]
newFile = "output_images/" + sys.argv[2]
ttFont = sys.argv[3]
fontSize = int(sys.argv[4])

fnt = ImageFont.truetype(ttFont, fontSize)

newImg = convertToASCII(originFile, fnt)

# Save the image.
newImg.save(newFile)
