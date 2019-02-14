# NFL Data Scraping

### scrape_game_data.py
* scrapes game ids from http://www.nfl.com/schedules/ into a list
* uses those game ids to find the json files with game data at http://www.nfl.com/liveupdate/game-center/
* downloads all the game files(named GAMEID.json) into a sub directory called GameData
### GetPlayerStats.py
* goes through each game file and collects all necessary data for individual players
* writes them to a dictionary
* writes data to a file named [PlayerStats.json](https://github.com/CoryPress/4883-SWTools-Press/blob/master/Assignments/A03/PlayerStats.json)
### GetTeamStats.py
* goes through each game file and collects all necessary data for teams
* writes them to a dictionary
* writes data to a file named [TeamStats.json](https://github.com/CoryPress/4883-SWTools-Press/blob/master/Assignments/A03/TeamStats.json)
### calculate_stats.py
* load PlayerStats.json and TeamStats.json
* uses that data to calculate desired stats


## My Output
```
Name: Cory Press
Assignment A03 - NFL Stats
Date: 2/13/2018

=============================================================================
1. Find the player(s) that played for the most teams.
=============================================================================

S.Graham played for a total of 8 teams.

=============================================================================
2. Find the player(s) that played for multiple teams in one year.
=============================================================================

A.Madison played for 3 in one season.
B.McCann played for 3 in one season.
B.Tate played for 3 in one season.
D.Thomas played for 3 in one season.
J.Forsett played for 3 in one season.
J.Freeny played for 3 in one season.
M.Addison played for 3 in one season.
M.McCrane played for 3 in one season.
R.Bullock played for 3 in one season.
R.Moss played for 3 in one season.
R.Mostert played for 3 in one season.
S.Andrus played for 3 in one season.
S.Draughn played for 3 in one season.
T.Cadet played for 3 in one season.
T.Choice played for 3 in one season.

=============================================================================
3. Find the player(s) that had the most yards rushed for a loss.
=============================================================================

M.Turk had a rush for -27 yards.

=============================================================================
4. Find the player(s) that had the most rushes for a loss.
=============================================================================

L.McCoy had 333 rushes for a loss.

=============================================================================
5. Find the player(s) with the most number of passes for a loss.
=============================================================================

D.Brees had 132 passes for a loss.

=============================================================================
6. Find the team with the most penalties.
=============================================================================

OAK had 1287 penalties since 2009.

=============================================================================
7. Find the team with the most yards in penalties.
=============================================================================

SEA lost 10867 due to penalties since 2009.

=============================================================================
8. Find the correlation between most penalized teams and games won / lost.
=============================================================================

r = 0.9690854548831433

=============================================================================
9. Average number of plays in a game.
=============================================================================

The average game had 176.8936329588015

=============================================================================
10. Longest field goal.
=============================================================================

M.Prater made a 64 yard field goal.

=============================================================================
11. Most field goals.
=============================================================================

S.Gostkowski made a total of 320 field goals.

=============================================================================
12. Most missed field goals.
=============================================================================

M.Crosby missed a total of 55 field goals.

=============================================================================
13. Most not caught passes by the intended reciever.
=============================================================================

L.Fitzgerald didn't catch a total of 2430 passes inteded for him.
```
* not sure of the accuracy of last stat. Only stats I could find where intended reciever of the pass, then I checked to see if he caught it. Unfortunately this doen't take into account anything about the accuracy of the pass.
