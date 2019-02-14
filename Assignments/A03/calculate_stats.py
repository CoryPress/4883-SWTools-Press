"""
Course: cmps 4883
Assignemt: A03
Date: 2/13/19
Github username: CoryPress
Repo url: https://github.com/CoryPress/4883-SWTools-Press
Name: Cory Press
Description: 
    Takes data from TeamStats.json and PlayerStats.json and
    finds several specific stats

"""

import os,sys
import json
import pprint as pp
import math

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






'''
Stat 1 & 2 - Find the player(s) that played for the most teams in total and in one seasons.
'''

maxTeams = 0
maxTeamsPlayers = []
maxTeamsInSeason = 0
maxTeamsInSeasonPlayers = []

print("Name: Cory Press")
print("Assignment A03 - NFL Stats")
print("Date: 2/13/2018\n")

for playerid, playerstats in PlayerData.items():
    if playerid != "0":
        PlayerTeams = []
        for season, seasonstats in playerstats.items():
            if season != "name":
                if len(seasonstats["teams"]) > maxTeamsInSeason:
                    maxTeamsInSeason = len(seasonstats["teams"])
                    maxTeamsInSeasonPlayers = []
                    maxTeamsInSeasonPlayers.append(playerstats["name"])
                elif len(seasonstats["teams"]) == maxTeamsInSeason:
                    maxTeamsInSeasonPlayers.append(playerstats["name"])
                for team in seasonstats["teams"]:
                    if team not in  PlayerTeams:
                        PlayerTeams.append(team)
    if len(PlayerTeams) > maxTeams:
        maxTeams = len(PlayerTeams)
        maxTeamsPlayers = []
        maxTeamsPlayers.append(playerstats["name"])
    elif len(PlayerTeams) == maxTeams:
        maxTeamsPlayers.append(playerstats["name"]) 
  

print("=============================================================================")
print("1. Find the player(s) that played for the most teams.")
print("=============================================================================\n")
maxTeamsPlayers.sort()
for player in maxTeamsPlayers:
    print(player + " played for a total of " + str(maxTeams) + " teams.")
print("\n=============================================================================")    
print("2. Find the player(s) that played for multiple teams in one year.")
print("=============================================================================\n")
maxTeamsInSeasonPlayers.sort()
for player in maxTeamsInSeasonPlayers:
    print(player + " played for " + str(maxTeamsInSeason) + " in one season.")
    
'''
stat 3 & 4 - find longest rush for a loss and most rushes for a loss
'''
worstRush = 0
worstRushPlayers = []
mostRushesForLoss = 0
mostRushesForLossPlayers = []

for playerid, playerstats in PlayerData.items():
    if playerid != "0":
        playerRushesForLoss = 0
        for season, seasonstats in playerstats.items():
            if season != "name":
                for rush in seasonstats["rushes"]:
                    if rush != None:
                        if rush < 0:
                            playerRushesForLoss += 1
                            if rush < worstRush:
                                worstRush = rush
                                worstRushPlayers = []
                                worstRushPlayers.append(playerstats["name"])
                            elif rush == worstRush:
                                worstRushPlayers.append(playerstats["name"])
        if playerRushesForLoss > mostRushesForLoss:
            mostRushesForLoss = playerRushesForLoss
            mostRushesForLossPlayers = []
            mostRushesForLossPlayers.append(playerstats["name"])
        elif playerRushesForLoss == mostRushesForLoss:
            mostRushesForLossPlayers.append(playerstats["name"])  
        
print("\n=============================================================================")
print("3. Find the player(s) that had the most yards rushed for a loss.")
print("=============================================================================\n")

worstRushPlayers.sort()
for player in worstRushPlayers:
    print(player + " had a rush for " + str(worstRush) + " yards.")

print("\n=============================================================================")    
print("4. Find the player(s) that had the most rushes for a loss.")
print("=============================================================================\n")

mostRushesForLossPlayers.sort()
for player in mostRushesForLossPlayers:
    print(player + " had " + str(mostRushesForLoss) + " rushes for a loss.")

    
'''
stat 4 - find player with most passes for a loss
'''

mostPassesForLoss = 0
mostPassesForLossPlayers = []

for playerid, playerstats in PlayerData.items():
    if playerid != "0":
        playerPassesForLoss = 0
        for season, seasonstats in playerstats.items():
            if season != "name":
                for pas in seasonstats["passes"]:
                    if pas != None:
                        if pas < 0:
                            playerPassesForLoss += 1
        if playerPassesForLoss > mostPassesForLoss:
            mostPassesForLoss = playerPassesForLoss
            mostPassesForLossPlayers = []
            mostPassesForLossPlayers.append(playerstats["name"])
        elif playerPassesForLoss == mostPassesForLoss:
            mostPassesForLossPlayers.append(playerstats["name"])
            
print("\n=============================================================================")    
print("5. Find the player(s) with the most number of passes for a loss.")
print("=============================================================================\n")

mostPassesForLossPlayers.sort()
for player in mostPassesForLossPlayers:
    print(player + " had " + str(mostPassesForLoss) + " passes for a loss.")
    
'''
stat 6 - 8 - Find team with most penaltys
'''

totPenalty= 0
totWins = 0
maxPenalty = 0
maxPenaltyYards = 0
maxPenaltyTeams = []
maxPenaltyYardsTeams = []

for teamabv, teamstats in TeamData.items():
    totPenalty = teamstats["penaltys"]
    totWins = teamstats["wins"]
    if teamstats["penaltys"] > maxPenalty:
        maxPenalty = teamstats["penaltys"]
        maxPenaltyTeams = []
        maxPenaltyTeams.append(teamabv)
    elif teamstats["penaltys"] == maxPenalty:
        maxPenaltyTeams.append(teamabv)
    if teamstats["penaltyYards"] > maxPenaltyYards:
        maxPenaltyYards = teamstats["penaltyYards"]
        maxPenaltyYardsTeams = []
        maxPenaltyYardsTeams.append(teamabv)
    elif teamstats["penaltyYards"] == maxPenaltyYards:
        maxPenaltyYardsTeams.append(teamabv)

avgWins = totWins/32
avgPenalty = totPenalty/32
sumNum = 0
sumWins2 = 0
sumPen2 = 0

for teamabv, teamstats in TeamData.items():
    sumNum += ((teamstats["penaltys"] - avgPenalty)*(teamstats["wins"] - avgWins))
    sumPen2 += (teamstats["penaltys"] - avgPenalty)*(teamstats["penaltys"] - avgPenalty)
    sumWins2 += (teamstats["wins"] - avgWins)*(teamstats["wins"] - avgWins)

r = sumNum / ( math.sqrt(sumPen2)*math.sqrt(sumWins2))
        

print("\n=============================================================================")    
print("6. Find the team with the most penalties.")
print("=============================================================================\n")

maxPenaltyTeams.sort()
for team in maxPenaltyTeams:
    print(team + " had " + str(maxPenalty) + " penalties since 2009.")

print("\n=============================================================================")    
print("7. Find the team with the most yards in penalties.")
print("=============================================================================\n")

maxPenaltyYardsTeams.sort()
for team in maxPenaltyYardsTeams:
    print(team + " lost " + str(maxPenaltyYards) + " due to penalties since 2009.")

print("\n=============================================================================")    
print("8. Find the correlation between most penalized teams and games won / lost.")
print("=============================================================================\n")

print("r = " + str(r))

mostMadeFG = 0
mostMadeFGPlayers = []
mostMissFG = 0
mostMissFGPlayers = []
longestFG = 0
longestFGPlayers = []

'''
Stat 9 - average plays in a game
'''

print("\n=============================================================================")    
print("9. Average number of plays in a game.")
print("=============================================================================\n")

print("The average game had " + str(PlayerData["0"]["plays"]/2670))

'''
Stat 10 - 11 - Longest field goal, most field goals made by a player, and most field
goals missed by a player
'''

for playerid, playerstats in PlayerData.items():
    if playerid != "0":
        playerFG = 0
        playerMissFG = 0
        for season, seasonstats in playerstats.items():
            if season != "name":
                for fg in seasonstats["fieldgoals"]:
                    if fg != None:
                        if fg > 0:
                            playerFG += 1
                        if fg > longestFG:
                            longestFG = fg
                            longestFGPlayers = []
                            longestFGPlayers.append(playerstats["name"])
                        elif fg == longestFG:
                            longestFGPlayers.append(playerstats["name"])
                        if fg == -1:
                            playerMissFG += 1
        if playerFG > mostMadeFG:
            mostMadeFG = playerFG
            mostMadeFGPlayers = []
            mostMadeFGPlayers.append(playerstats["name"])
        elif playerFG == mostMadeFG:
            mostMadeFGPlayers.append(playerstats["name"])
        
        if playerMissFG > mostMissFG:
            mostMissFG = playerMissFG
            mostMissFGPlayers = []
            mostMissFGPlayers.append(playerstats["name"])
        elif playerMissFG == mostMissFG:
            mostMissFGPlayers.append(playerstats["name"])
            


print("\n=============================================================================")    
print("10. Longest field goal.")
print("=============================================================================\n")

longestFGPlayers.sort()
for player in longestFGPlayers:
    print(player + " made a " + str(longestFG) + " yard field goal.")


print("\n=============================================================================")    
print("11. Most field goals.")
print("=============================================================================\n")

mostMadeFGPlayers.sort()
for player in mostMadeFGPlayers:
    print(player + " made a total of " + str(mostMadeFG) + " field goals.")


print("\n=============================================================================")    
print("12. Most missed field goals.")
print("=============================================================================\n")

mostMissFGPlayers.sort()
for player in mostMissFGPlayers:
    print(player + " missed a total of " + str(mostMissFG) + " field goals.")
    
    
'''
Stat 9 - most dropped passes
'''
    

mostDroppedPasses = 0
mostDroppedPassesPlayers = []

for playerid, playerstats in PlayerData.items():
    if playerid != "0":
        playerDrops = 0
        for season, seasonstats in playerstats.items():
            if season != "name":
                playerDrops += seasonstats["droppedPasses"]
        if mostDroppedPasses < playerDrops:
            mostDroppedPasses = playerDrops
            mostDroppedPassesPlayers = []
            mostDroppedPassesPlayers.append(playerstats["name"])
        elif mostDroppedPasses == playerDrops:
            mostDroppedPassesPlayers.append(playerstats["name"])
    

print("\n=============================================================================")    
print("13. Most not caught passes by the intended reciever.")
print("=============================================================================\n")

mostDroppedPassesPlayers.sort()
for player in mostDroppedPassesPlayers:
    print(player + " didn't catch a total of " + str(mostDroppedPasses) + " passes inteded for him.")
    
