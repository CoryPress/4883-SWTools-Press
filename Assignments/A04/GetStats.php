<?php

//Course: cmps 4883
//Assignemt: A04
//Date: 3/05/19
//Github username: CoryPress
//Repo url: https://github.com/CoryPress/4883-SWTools-Press
//Name: Cory Press
//Description: 
//    Using queries list in queries.sql performs them on the cs2 server and prints
//    them out in formated ASCII tables

//Connect to mysql
$host = "localhost";             // because we are ON the server
$user = "***********";        // user name

// Get username and password from slack
// The DB username and pass not the ones
// I sent you to log into the server.
$password = "************";         // password 
$database = "nfl_data";              // database 
$mysqli = mysqli_connect($host, $user, $password, $database);

if (mysqli_connect_errno($mysqli)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}


/**
 * This function runs a SQL query and returns the data in an associative array
 * that looks like:
 * $response [
 *      "success" => true or false
 *      "error" => contains error if success == false
 *      "result" => associative array of the result
 * ]
 *
 */
function runQuery($mysqli,$sql){
    $response = [];

    // run the query
    $result = $mysqli->query($sql);

    // If we were successful
    if($result){
        $response['success'] = true;
        // loop through the result printing each row
        while($row = $result->fetch_assoc()){
            $response['result'][] = $row;
        }
        $result->free();
    }else{
        $response['success'] = false;
        $response['error'] = $mysqli->error;
    }

    return $response;
}

echo "<pre>";   // so whitespace matters

//header
print("Name: Cory Press
Assignment: A04 - Nfl Stats 
Date: 3/5/2019
==================================================================================\n\n");


//Question 1
//header
print("Teams played for:

 #  Player ID      Name            # Teams
===========================================\n");

//run query
$sql = "SELECT id, name, COUNT(DISTINCT club) AS cnt 
FROM players 
GROUP BY id 
ORDER BY cnt DESC, name ASC
limit 10";

$response = runQuery($mysqli, $sql);

//format row string
$format = '%2d  %-12s   %-15s %-3d';

$index = 0;
$previous = 33;
if($response['success']){
    //print each row
    foreach($response['result'] as $row){
        //if tie
        if($row['cnt'] < $previous){
            $index = $index + 1;
            $previous = $row['cnt'];
        }
        echo sprintf($format, $index, $row['id'], $row['name'], $row['cnt']);
        print("\n");
    }
}


//Question 2
print("\n\nTop 5 rushing players in a single season:
    
 #  Player ID     Name            Season    Yards
==================================================\n");
    
$sql = "SELECT playerid, IdToName.name, players_stats.season, SUM(yards) as SeasonYards 
    FROM players_stats left join (select id, name from players group by id) as IdToName 
    on players_stats.playerid = IdToName.id 
    WHERE statid = 10 or statid = 11 
    group by playerid, season 
    order by SeasonYards DESC, IdToName.name ASC
    limit 5";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-12s  %-15s %-4s      %-5d';

$index = 0;
$previous = 100000;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['SeasonYards'] < $previous){
            $index = $index + 1;
            $previous = $row['SeasonYards'];
        }
        echo sprintf($format, $index, $row['playerid'], $row['name'], $row['season'],
            $row['SeasonYards']);
        print("\n");
    }
}

//Question 3
print("\n\nTop 5 worst passing yards:

 #  Player ID     Name            Season    Yards
==================================================\n");

$sql = "SELECT playerid, IdToName.name, players_stats.season, SUM(yards) as SeasonYards
FROM players_stats left join (select id, name from players group by id) as IdToName 
on players_stats.playerid = IdToName.id 
WHERE statid = 15 or statid = 16 
group by playerid, season 
order by SeasonYards ASC, IdToName.name ASC 
limit 5";

$response = runQuery($mysqli, $sql);

$index = 0;
$previous = -10000;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['SeasonYards'] > $previous){
            $index = $index + 1;
            $previous = $row['SeasonYards'];
        }
        echo sprintf($format, $index, $row['playerid'], $row['name'], $row['season'],
            $row['SeasonYards']);
        print("\n");
    }
}

//Question 4
print("\n\nTop 5 most rushes for a loss:

 #  Player ID     Name          Rush for loss
==============================================\n");

$sql = "SELECT playerid, IdToName.name, count(*) badRushes
            FROM players_stats left join (select id, name from players group by id) as IdToName
            on players_stats.playerid = IdToName.id
            where (statid = 10 or statid = 11) and yards < 0
            group by playerid
            order by badRushes DESC
            LIMIT 5";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-12s  %-13s %-5d';

$index = 0;
$previous = 10000;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['badRushes'] < $previous){
            $index = $index + 1;
            $previous = $row['badRushes'];
        }
        echo sprintf($format, $index, $row['playerid'], $row['name'], $row['badRushes']);
        print("\n");
    }
}


//Question 5
print("\n\nTop 5 most penalized teams:
    
 #  Team   Penalties
=====================\n");

$sql = "SELECT club, sum(pen) as Penaltys
    FROM game_totals
    group by club
    order by Penaltys DESC
    LIMIT 5";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-4s   %-5d';

$index = 0;
$previous = 10000;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['Penaltys'] < $previous){
            $index = $index + 1;
            $previous = $row['Penaltys'];
        }
        echo sprintf($format, $index, $row['club'], $row['Penaltys']);
        print("\n");
    }
}


//Question 6
print("\n\nTop 10 seasons with highest penalties/game:

 #  Season  Penalties  AVG Penalties
=====================================\n");

$sql = "SELECT season, sum(pen) as Penaltys, sum(pen) / count(gameid) as averagePenaltys 
            FROM game_totals 
            group by season 
            order by averagePenaltys 
            DESC LIMIT 10";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-5s   %-5d      %-2.3f';

$index = 0;
$previous = 10000;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['averagePenaltys'] < $previous){
            $index = $index + 1;
            $previous = $row['averagePenaltys'];
        }
        echo sprintf($format, $index, $row['season'], $row['Penaltys'], $row['averagePenaltys']);
        print("\n");
    }
}


//Question 7
print("\n\nTop 10 team seasons with lowest plays/game:

 #  Team  Season  AVG Plays
============================\n");

$sql = "SELECT clubid, GameSeason.season, count(playid) / count(DISTINCT plays.gameid) as averagePlays 
            FROM plays left join (SELECT gameid, season from game_totals group by gameid) as GameSeason 
            on plays.gameid = GameSeason.gameid 
            group by clubid, season 
            ORDER by averagePlays ASC 
            limit 10";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-5s %-5s   %-2.3f';

$index = 0;
$previous = 0;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['averagePlays'] > $previous){
            $index = $index + 1;
            $previous = $row['averagePlays'];
        }
        echo sprintf($format, $index, $row['clubid'], $row['season'], $row['averagePlays']);
        print("\n");
    }
}


//Question 8
print("\n\nTop 5 players with most field goals over 40 yards:

 #  Player ID    Name           +40 FG
=======================================\n");

$sql = "SELECT playerid, IdToName.name, count(*) longFGs
            FROM players_stats left join (select id, name from players group by id) as IdToName
            on players_stats.playerid = IdToName.id
            where statid = 70 and yards > 40
            group by playerid
            order by longFGs DESC
            LIMIT 5";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-12s %-13s   %-3d';

$index = 0;
$previous = 100000;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['longFGs'] < $previous){
            $index = $index + 1;
            $previous = $row['longFGs'];
        }
        echo sprintf($format, $index, $row['playerid'], $row['name'], $row['longFGs']);
        print("\n");
    }
}


//Question 9
print("\n\nTop 5 players with the shortest average field goal length:

 #  Player ID    Name           AVG Yards
==========================================\n");

$sql = "SELECT playerid, IdToName.name, sum(Yards)/count(*) as averageLength
            FROM players_stats left join (select id, name from players group by id) as IdToName
            on players_stats.playerid = IdToName.id
            where statid = 70
            group by playerid
            order by averageLength ASC
            LIMIT 5";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-12s %-13s  %-2.3f';

$index = 0;
$previous = 0;
if($response['success']){
    foreach($response['result'] as $row){
        if($row['averageLength'] > $previous){
            $index = $index + 1;
            $previous = $row['averageLength'];
        }
        echo sprintf($format, $index, $row['playerid'], $row['name'], $row['averageLength']);
        print("\n");
    }
}

//Question 10
print("\n\nWorst NFL teams by win percentage

 #  Team   Win %
==================\n");

$sql = "SELECT game_totals.club, (count(*) / TotalGames) * 100 as winPrct
            from game_totals left join (select club, count(*) as TotalGames FROM game_totals group by club) as TeamsGames
            on game_totals.club = TeamsGames.club
            where wonloss = \"won\"
            group by club
            order by winPrct ASC";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-4s   %-2.3f';

$index = 32;
$previous = 0;
if($response['success']){
    foreach($response['result'] as $row){
        echo sprintf($format, $index, $row['club'], $row['winPrct']);
        print("\n");
        $index = $index - 1;
    }
}


//Question 11
print("\n\nTop 5 most common last names in the NFL:

 #  Last Name      Occurences
==============================\n");

$sql = "SELECT SUBSTRING(name, 3) as LastName, count(*) as total
            FROM players
            GROUP BY LastName
            Order by total DESC
            limit 5";

$response = runQuery($mysqli, $sql);

$format = '%2d  %-13s  %-3d';

$index = 32;
$previous = 0;
if($response['success']){
    foreach($response['result'] as $row){
        echo sprintf($format, $index, $row['LastName'], $row['total']);
        print("\n");
        $index = $index - 1;
    }
}
