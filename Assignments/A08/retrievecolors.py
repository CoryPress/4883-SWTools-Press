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

for color in page.find_all('div', {'style':"float:left;display:inline;font-size:90%;margin:1px 5px 1px 5px;width:11em; height:6em;text-align:center;padding:auto;"}):
    name = ""
    a = color.find_all('a', {'':""})
    if len(a) > 0:
        string = str(a[0])
        string = string.replace('<', '>')
        strings = string.split('>')
        name = strings[-3]
    colors[name] = {}
    if name != "":
        p = color.find_all('p', {'':""})
        string = str(p[0])
        string = string.replace(',', '(')
        string = string.replace(')', '(')
        strings = string.split('(')
        
        colors[name]['r'] = int(strings[1])
        colors[name]['g'] = int(strings[2])
        colors[name]['b'] = int(strings[3])

f = open("color.json","w")
f.write(json.dumps(colors))
f.close()
