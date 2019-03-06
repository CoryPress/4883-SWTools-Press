import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def convertToASCII(originF, fnt):

    #open image and convert to grayscale
    im = Image.open(originF)
    im = im.convert("L")

    w,h = im.size
    
    ascii_chars = [ 'y', 'd', 'c', '6', 'W', 'p', 'm', 'q', 'w', 'n', 'N']

    newImg = Image.new('RGBA', (w*fnt.size, h*fnt.size), (255,255,255,255))

    
    drawOnMe = ImageDraw.Draw(newImg)

    imlist = list(im.getdata())

    x = 0
    y = 0
    for val in imlist:
        ch = ascii_chars[val // 25]
        drawOnMe.text((x,y), ch, font=fnt, fill=(0,0,0,255))
        x += fnt.size
        if x >= newImg.size[0]:
            sys.stdout.write(".")
            x = 0
            y += fnt.size
    

    return newImg


    


originFile = "input_images/" + sys.argv[1]
newFile = "output_images/" + sys.argv[2]
ttFont = sys.argv[3]
fontSize = int(sys.argv[4])

fnt = ImageFont.truetype(ttFont, fontSize)



newImg = convertToASCII(originFile, fnt)

#newImg.show()

# Save the image.
newImg.save(newFile)