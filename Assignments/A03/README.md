# NFL Data Scraping

### scrape_game_data.py
* scrapes game ids from http://www.nfl.com/schedules/ into a list
* uses those game ids to find the json files with game data at http://www.nfl.com/liveupdate/game-center/
* downloads all the game files(named GAMEID.json) into a sub directory called GameData
### GetPlayerStats.py
* goes through each game file and collects all necessary data for individual players
* writes them to a dictionary
* writes data to a file named PlayerStats.json
### GetTeamStats.py
* goes through each game file and collects all necessary data for teams
* writes them to a dictionary
* writes data to a file named TeamStats.json
### calculate_stats.py
* load PlayerStats.json and TeamStats.json
* uses that data to calculate desired stats
