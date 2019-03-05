
`1`
SELECT id, NAME , COUNT(DISTINCT club) AS cnt 
FROM players 
GROUP BY id 
ORDER BY cnt DESC, name ASC
limit 10

`2`
SELECT playerid, IdToName.name, players_stats.season, SUM(yards) as SeasonYards 
FROM players_stats left join (select id, name from players group by id) as IdToName 
on players_stats.playerid = IdToName.id 
WHERE statid = 10 or statid = 11 
group by playerid, season 
order by SeasonYards DESC, IdToName.name ASC
limit 5

`3`
SELECT playerid, IdToName.name, players_stats.season, SUM(yards) as SeasonYards
FROM players_stats left join (select id, name from players group by id) as IdToName 
on players_stats.playerid = IdToName.id 
WHERE statid = 15 or statid = 16 
group by playerid, season 
order by SeasonYards ASC, IdToName.name ASC 
limit 5

`4`
SELECT playerid, IdToName.name, count(*) badRushes
FROM players_stats left join (select id, name from players group by id) as IdToName
on players_stats.playerid = IdToName.id
where (statid = 10 or statid = 11) and yards < 0
group by playerid
order by badRushes DESC

`5`
SELECT club, sum(pen) as Penaltys
FROM game_totals
group by club
order by Penaltys DESC
LIMIT 5

`6`
SELECT season, sum(pen) as Penaltys, sum(pen) / count(gameid) as averagePenaltys 
FROM game_totals 
group by season 
order by averagePenaltys 
DESC LIMIT 10

`7`
SELECT clubid, GameSeason.season, count(playid) / count(DISTINCT plays.gameid) as averagePlays 
FROM plays left join (SELECT gameid, season from game_totals group by gameid) as GameSeason 
on plays.gameid = GameSeason.gameid 
group by clubid, season 
ORDER by averagePlays ASC 
limit 10

`8`
SELECT playerid, IdToName.name, count(*) longFGs
FROM players_stats left join (select id, name from players group by id) as IdToName
on players_stats.playerid = IdToName.id
where statid = 70 and yards > 40
group by playerid
order by longFGs DESC
LIMIT 5

`9`
SELECT playerid, IdToName.name, sum(Yards)/count(*) as averageLength
FROM players_stats left join (select id, name from players group by id) as IdToName
on players_stats.playerid = IdToName.id
where statid = 70
group by playerid
order by averageLength ASC
LIMIT 5

`10`
SELECT game_totals.club, count(*) / TotalGames as winPrct
from game_totals left join (select club, count(*) as TotalGames FROM game_totals group by club) as TeamsGames
on game_totals.club = TeamsGames.club
where wonloss = "won"
group by club
order by winPrct ASC

`11`
SELECT SUBSTRING(name, 3) as LastName, count(*) as total
FROM players
GROUP BY LastName
Order by total DESC
limit 5

