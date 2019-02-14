import os,sys
import json
import pprint as pp

"""
Assumes you have all of your game data in a folder called '/json_data/live_update_data'
and your files are named gameid.json where gameid can be something like 2009102505.json
"""



#from dr.griffin - corrects team codes for teams that changed mascots/location
TeamCodes ={ "MIN": "MIN", "MIA": "MIA", "CAR": "CAR", "ATL": "ATL", "DET": "DET", "CIN": "CIN", "NYJ": "NYJ", 
                   "DEN": "DEN", "BAL": "BAL", "NYG": "NYG", "OAK": "OAK", "TEN": "TEN", "NO": "NO", "DAL": "DAL", "NE": "NE",
                   "BUF": "BUF", "SEA": "SEA", "CHI": "CHI", "TB": "TB", "JAX": "JAX", "STL": "LA", "CLE": "CLE", "HOU": "HOU",
                   "GB": "GB", "WAS": "WAS", "JAC": "JAX", "KC": "KC", "PHI": "PHI", "PIT": "PIT", "LA": "LA", "LAC": "LAC", 
                   "IND": "IND", "ARI": "ARI", "SF": "SF", "SD": "LAC"}

"""
Returns a list of files in given directory
"""
def getFiles(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            files.append(os.path.join(dirname, filename))

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')
    return files


"""
Checks to see if it is json
"""
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

"""
Tries to open a file 
"""
def openFileJson(path):
    try:
      f = open(path, "r")
      data = f.read()
      if is_json(data):
          return json.loads(data)
      else:
          print ("Error: Not json.")
          return {}
    except IOError:
        print ("Error: Game file doesn't exist.")
        return {}
    
    
"""
Gets Season given the file name
"""
def getSeason(filename):
    year = int(filename[11:15])
    if int(filename[15:17]) in [1, 2]:
        year -= 1
    return year
    


path = './GameData/'
files = getFiles(path)

files = sorted(files)

TeamData = {}

plays = 0
games = 0

# loop through files
for file in files:
    
    #progress
    if games%267 == 0:
        print("progress = %" + str(games/2670*100))
    games += 1

    # read in json data and convert to dictionary
    data = openFileJson(file)

    season = getSeason(file)

    # pull out the game id and game data
    for gameid,gamedata in data.items():
        if gameid != "nextupdate":
            #get home and away team abreviation and stats
            homeabrv = TeamCodes[gamedata["home"]["abbr"]]
            awayabrv = TeamCodes[gamedata["away"]["abbr"]]
            homestats = gamedata["home"]["stats"]["team"]
            awaystats = gamedata["away"]["stats"]["team"]
            # if team teams first appearance create dictionary
            if homeabrv not in TeamData:
                TeamData[homeabrv] = {}
                TeamData[homeabrv]["gamesplayed"] = 0
                TeamData[homeabrv]["wins"] = 0
                TeamData[homeabrv]["penaltys"] = 0
                TeamData[homeabrv]["penaltyYards"] = 0
            if awayabrv not in TeamData:
                TeamData[awayabrv] = {}
                TeamData[awayabrv]["gamesplayed"] = 0
                TeamData[awayabrv]["wins"] = 0
                TeamData[awayabrv]["penaltys"] = 0
                TeamData[awayabrv]["penaltyYards"] = 0
            #add one to games played
            TeamData[homeabrv]["gamesplayed"] += 1
            TeamData[awayabrv]["gamesplayed"] += 1
            #add penaltys to total
            TeamData[homeabrv]["penaltys"] += homestats["pen"]
            TeamData[homeabrv]["penaltyYards"] += homestats["penyds"]
            TeamData[awayabrv]["penaltys"] += awaystats["pen"]
            TeamData[awayabrv]["penaltyYards"] += awaystats["penyds"]
            
            #find winner and add one to winning teams total wins
            if gamedata["home"]["score"]["T"] > gamedata["away"]["score"]["T"]:
                TeamData[homeabrv]["wins"] += 1
            else:
                TeamData[awayabrv]["wins"] += 1

pp.pprint(TeamData)

#write player data to a new file to be processed to find nessicary stats                                     
f = open("./TeamStats.json","w")
f.write(json.dumps(TeamData))
f.close()
