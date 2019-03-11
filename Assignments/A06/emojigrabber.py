# Cory Press
# Downloads all emoji images from https://www.webfx.com/tools/emoji-cheat-sheet/
# using beautifulscraper and urllib.request

import beautifulscraper
import sys
import os
import urllib.request

scraper = beautifulscraper.BeautifulScraper()


url = 'https://www.webfx.com/tools/emoji-cheat-sheet/'

page = scraper.go(url)

#if not already created create emoji subdirectory to store images
newfolderpath = "./emojis/"
if not os.path.exists(newfolderpath):
    os.makedirs(newfolderpath) 

numEmojis = 0
#loop through all emojis
for emoji in page.find_all('span', {'class':"emoji"}):
    image_path = emoji['data-src']
    file_name = image_path[16:]

    #request image and same to new file
    urllib.request.urlretrieve(url+image_path, newfolderpath+file_name)

    #progress
    numEmojis += 1
    if numEmojis%10 == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
    
print(numEmojis)
