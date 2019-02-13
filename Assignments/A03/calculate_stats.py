import os,sys
import json
import pprint as pp

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
Checks to see if it is json
"""
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

path = "./PlayerStats.json"
PlayerData = openFileJson(path)

path = "./TeamStats.json"
TeamData = openFileJson(path)

#Stat 1 & 2- Find the player(s) that played for the most teams.
PlayerTeams = {}
for playerid, playerstats in PlayerData.items():
    if playerid != "0":
        if playerid not in PlayerTeams:
            PlayerTeams[playerid] = {}
            PlayerTeams[playerid]["name"] = playerstats["name"]
            PlayerTeams[playerid]["teams"] = []
            PlayerTeams[playerid]["MaxTeamsInASeason"] = 0
        for season, seasonstats in playerstats.items():
            if season != "name":
                if len(seasonstats["teams"]) > PlayerTeams[playerid]["MaxTeamsInASeason"]:
                    PlayerTeams[playerid]["MaxTeamsInASeason"] = len(seasonstats["teams"])
                for team in seasonstats["teams"]:
                    if team not in  PlayerTeams[playerid]["teams"]:
                        PlayerTeams[playerid]["teams"].append(team)
  

maxTeams = 0
maxTeamsPlayers = []
maxTeamsInSeason = 0
maxTeamsInSeasonPlayers = []
for playerid, playerstats in PlayerTeams.items():
    if len(playerstats["teams"]) > maxTeams:
        maxTeams = len(playerstats["teams"])
        maxTeamsPlayers = []
        maxTeamsPlayers.append(playerstats["name"])
    elif len(playerstats["teams"]) == maxTeams:
        maxTeamsPlayers.append(playerstats["name"])
        
    if playerstats["MaxTeamsInASeason"] > maxTeamsInSeason:
        maxTeamsInSeason = playerstats["MaxTeamsInASeason"]
        maxTeamsInSeasonPlayers = []
        maxTeamsInSeasonPlayers.append(playerstats["name"])
    elif playerstats["MaxTeamsInASeason"] == maxTeamsInSeason:
        maxTeamsInSeasonPlayers.append(playerstats["name"])

print("=============================================================================")
print("1. Find the player(s) that played for the most teams.\n")
maxTeamsPlayers.sort()
for player in maxTeamsPlayers:
    print(player + " played for a total of " + str(maxTeams) + ".")
print("\n=============================================================================")    
print("2. Find the player(s) that played for multiple teams in one year.\n")
maxTeamsInSeasonPlayers.sort()
for player in maxTeamsInSeasonPlayers:
    print(player + " played for " + str(maxTeamsInSeason) + " in one season.")

