#Cory Press
#downloads all avliable(2009 - present) NFL game statistics
#from NFL.com

from beautifulscraper import BeautifulScraper
import urllib
import json
import sys
import time
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
        
        #depending on playtime? gameid is in diferent class
        #  and 2009 has complete different classes
        divs = page.find_all('div',{"class":"schedules-list-content post expandable primetime type-reg pro-legacy"})
        divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable type-reg pro-legacy"}))
        divs.extend( page.find_all('div',{"class":"schedules-list-content post primetime type-reg pro-legacy"}))
        divs.extend( page.find_all('div',{"class":"schedules-list-content post type-reg pro-legacy"}))
        
        for div in divs:
            games += 1
            gameids.append(div['data-gameid'])
            
            
#
# POSTSEASON
#

#get ids for just 2009 so i dont waste time searching for
#classes in other years that they dont have
url = "http://www.nfl.com/schedules/2009/POST" 
page = scraper.go(url)



for year in range (2009, 2019):
    print("progress = %" + str(games/2670*100))
    
    url = "http://www.nfl.com/schedules/" + str(year) + "/POST" 
    page = scraper.go(url)
    
    #all the different game types for postseason
    divs = page.find_all('div',{"class":      "schedules-list-content post type-wc pro-legacy"})
    divs.extend( page.find_all('div',{"class":"schedules-list-content post primetime type-wc pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post type-div pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post type-con pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post type-sb pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable primetime type-wc pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable type-wc pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable type-div pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable primetime type-div pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable type-con pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable type-sb pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable primetime type-sb pro-legacy"}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable type-sb "}))
    divs.extend( page.find_all('div',{"class":"schedules-list-content post expandable primetime type-sb "}))
    
    for div in divs:
        games += 1
        gameids.append(div['data-gameid'])

#check that i got all games
#should be 2670 = (32(teams) x 16(games) / 2(for repeats) + 11(postseason))*10(seasons)
print(len(gameids))

#
# Download all game json files
#

games = 0
for gameid in gameids:
    #progress
    if games%25 == 0:
        print("progress = %" + str(games/2670*100))
    games += 1
    
    with urllib.request.urlopen("http://www.nfl.com/liveupdate/game-center/"+gameid+"/"+gameid+"_gtd.json") as url:
        data = json.loads(url.read().decode())
    
    f = open("./GameData/game_"+gameid+".json","w")
    f.write(json.dumps(data))
    f.close()

