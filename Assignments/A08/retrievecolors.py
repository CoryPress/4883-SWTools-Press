#   
#   retrievecolors.py
#       Cory Press 
#       retrieves all named colors listed by wikipedia and store their information in colors.json
#   
#
import beautifulscraper
import sys
import os
import urllib.request
import re
import json

scraper = beautifulscraper.BeautifulScraper()
    
colors = {}
    

url = "https://en.wikipedia.org/wiki/List_of_colors_(compact)"
page = scraper.go(url)

#process through page to ge color name and rgb values
for block in page.find_all('div', {'style':"float:left;display:inline;font-size:90%;margin:1px 5px 1px 5px;width:11em; height:6em;text-align:center;padding:auto;"}):
    name = ""
    a = block.find_all('a', {'':""})
    if len(a) > 0:
        #split string to find name
        string = str(a[0])
        string = string.replace('<', '>')
        strings = string.split('>')
        name = strings[-3]
    colors[name] = {}
    if name != "":
        p = block.find_all('p', {'':""})
        string = str(p[0])

        #split string to get individual rgb values
        string = string.replace(',', '(')
        string = string.replace(')', '(')
        strings = string.split('(')
        
        colors[name]['r'] = int(strings[1])
        colors[name]['g'] = int(strings[2])
        colors[name]['b'] = int(strings[3])

f = open("colors.json","w")
f.write(json.dumps(colors))
f.close()
