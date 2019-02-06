# NFL Data Scraping

### scrape_game_data.py
* scrapes game ids from http://www.nfl.com/schedules/ into a list
* uses those game ids to find the json files with game data at http://www.nfl.com/liveupdate/game-center/
* downloads all the game files(named game_GAMEID.json) into a sub directory called GameData
