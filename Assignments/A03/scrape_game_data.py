#Cory Press
#downloads all avliable(2009 - present) NFL game statistics
#from NFL.com

from beautifulscraper import BeautifulScraper
import urllib
import json
import sys
import time
import os
scraper = BeautifulScraper()

gameids = []

#
#REGULAR SEASON
#

games = 0

for year in range (2009, 2019):
    print("progress = %" + str(games/2670*100))
    
    for week in range(1, 18):
        url = "http://www.nfl.com/schedules/" + str(year) + "/REG" +str(week)
        page = scraper.go(url)
        
        #get all game classes
        divs = page.find_all('div',{"class":"schedules-list-content"})
        
        #get gameid from those clases
        for div in divs:
            games += 1
            gameids.append(div['data-gameid'])
            

#
# POSTSEASON
#

for year in range (2009, 2019):
    print("progress = %" + str(games/2670*100))
    
    url = "http://www.nfl.com/schedules/" + str(year) + "/POST" 
    page = scraper.go(url)
    
    #get all game class
    divs = page.find_all('div',{"class": "schedules-list-content"})
    
    for div in divs:
        #check to make sure not pro bowl
        if div["class"][-2] != "type-pro":
            games += 1
            gameids.append(div['data-gameid'])
        
#check that i got all games
#should be 2670 = (32(teams) x 16(games) / 2(for repeats) + 11(postseason))*10(seasons)
print(len(gameids)) 


#
# Download all game json files
#

#create GameData folder
newfolderpath = "./GameData/"
if not os.path.exists(newfolderpath):
    os.makedirs(newfolderpath)        


games = 0
for gameid in gameids:
    #progress
    if games%100 == 0:
        print("progress = %" + str(games/2670*100))
    games += 1
    
    with urllib.request.urlopen("http://www.nfl.com/liveupdate/game-center/"+gameid+"/"+gameid+"_gtd.json") as url:
        data = json.loads(url.read().decode())
    
    f = open("./GameData/"+gameid+".json","w")
    f.write(json.dumps(data))
    f.close()

