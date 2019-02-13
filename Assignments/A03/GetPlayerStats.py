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

PlayerData = {}

plays = 0
games = 0

# loop through files
for file in files:
    
    #progress
    if games%50 == 0:
        print("progress = %" + str(games/2670*100))
    games += 1

    # read in json data and convert to dictionary
    data = openFileJson(file)

    season = getSeason(file)

    # pull out the game id and game data
    for gameid,gamedata in data.items():
        #if 
        if gameid != "nextupdate":
            # go straight for the drives
            for driveid,drivedata in gamedata['drives'].items():
                #if not final drive
                if driveid != 'crntdrv':
                    #for all plays in the drive
                    for playid,playdata in drivedata['plays'].items():
                        plays += 1
                        #for each player that had a stat in each play
                        for playerid, player in playdata["players"].items():
                            #if not team stat
                            if playerid != '0':
                                #for each different stat a player had on that play
                                for playerstat in player:
                                    #if first appearance of a player create new dictionary for that player 
                                    # and for that players current season
                                    if playerid not in PlayerData:
                                        PlayerData[playerid] = {}
                                        PlayerData[playerid]["name"] = playerstat["playerName"]
                                        PlayerData[playerid][season] = {}
                                        PlayerData[playerid][season]["teams"] = []
                                        PlayerData[playerid][season]["teams"].append(TeamCodes[playerstat["clubcode"]])
                                        PlayerData[playerid][season]["rushes"] = []
                                        PlayerData[playerid][season]["passes"] = []
                                        PlayerData[playerid][season]["droppedPasses"] = 0
                                        PlayerData[playerid][season]["fieldgoals"] = []
                                    #if players first appearance in season create new dictionary
                                    if season not in PlayerData[playerid]:
                                        PlayerData[playerid][season] = {}
                                        PlayerData[playerid][season]["teams"] = []
                                        PlayerData[playerid][season]["teams"].append(TeamCodes[playerstat["clubcode"]])
                                        PlayerData[playerid][season]["rushes"] = []
                                        PlayerData[playerid][season]["passes"] = []
                                        PlayerData[playerid][season]["droppedPasses"] = 0
                                        PlayerData[playerid][season]["fieldgoals"] = []
                                    #if first appearance on a certain team this season add to teams
                                    if TeamCodes[playerstat["clubcode"]] not in PlayerData[playerid][season]["teams"]:
                                        PlayerData[playerid][season]["teams"].append(TeamCodes[playerstat["clubcode"]])
                                    #if player made a rush add yard of that yards rushed that play to season list
                                    # for rushes
                                    if playerstat["statId"] in [10, 11]:
                                        PlayerData[playerid][season]["rushes"].append(playerstat["yards"])
                                    #if player completed a pass add yards of that pass to season list
                                    # for passes
                                    if playerstat["statId"] in [15, 16]:
                                        PlayerData[playerid][season]["passes"].append(playerstat["yards"])
                                    #if player missed field goal and a -1 to list for field goal to signify a
                                    # misssed field goal
                                    if playerstat["statId"] == 69:
                                        PlayerData[playerid][season]["fieldgoals"].append(-1)
                                    #if made field goal add field goal length to the list for field goals
                                    if playerstat["statId"] == 70:
                                        PlayerData[playerid][season]["fieldgoals"].append(playerstat["yards"])
                                    #if player thrown to did complete the pass add 1 to dropped passes
                                    if playerstat["statId"] == 115:
                                        for playerstat in player:
                                            if(playerstat["statId"] not in [21, 22]):
                                                PlayerData[playerid][season]["droppedPasses"] += 1
                                                
#write player data to a new file to be processed to find nessicary stats                                     
f = open("./PlayerStats.json","w")
f.write(json.dumps(PlayerData))
f.close()                                       
