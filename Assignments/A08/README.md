# A08 - Image Mosaic

### get_dominant_colors.py - 
* maps all images in imagefolder to their most dominant color and save them in a json file so multiple mosaics can be created without having to process all the image twice
```
#       args-
#           imagefolder - folder that contains image you want to make your mosaic out of
#           n           - number of clusters
#       output-
#           dominant_colors_*imagefloder*.json - maps all images in imagefolder to their most
#               dominant color
```
### image_to_mosaic.py - 
* creates a mosaic out of the image in folder(must run get_dominant_colors.py first tp generate json file that will be used here) by replaces number of a square of square of pixels, side = pixels, a replaces it with a size x size image from the folder thats dominant color is closest to the average color of that square
```
#       args-
#           image       - image to be made into a mosaic
#           folder      - folder that contains image you want to make your mosaic out of
#           pixels      - number of pixels the will be replaced by one image (closer to one the better)
#           size        - size of each sub image
#       output-
#           *image*_mosaic.png - creates a mosaic of image out of the images in folder
#
```
