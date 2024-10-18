import json
import csv
import os
import datetime


def leagueSep():
    gc = []
    challengers = []
    vct = []
    misc = []

    dataPack = [gc, challengers, vct, misc]
    nameKey = ['game_changers_data', 'challengers_data', 'vct_data', 'misc_data']

    with open('dataCleaned2023-2024.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    f.close()

    for i in data:
        tmp = i["tournament"]
        
        if("Game Changers" in tmp):
            gc.append(i)
        elif("Challengers League" in tmp):
            challengers.append(i)
        elif("Champions Tour" in tmp):
            vct.append(i)
        else:
            misc.append(i)

    for i in range(4):
        with open(f'{nameKey[i]}.json', 'w', encoding="utf-8") as j:
            json.dump(dataPack[i], j, ensure_ascii=False)

def chunkSep():
    with open('game data/tournament/game_changers_data.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    f.close()

    count = 1

    for i in data:
        with open(f'export/gc_chunked/chunk{count}.txt', 'w', encoding="utf-8") as j:
            json.dump(i, j, ensure_ascii=False)
        j.close()

        count += 1

def chunkSepPt2():
    with open('game data/tournament/game_changers_data.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    f.close()

    count = 1

    for i in data:
        '''
        teams = i["teams"] #dictionary of 2 teams
        relativeDate = i["date"]
        event = i["event"]
        tour = i["tournament"]

        team1 = teams[0]
        team2 = teams[1]

        winner = ""

        if(team1["won"] == "true" or team1["won"] == True):
            winner = team1["name"]
        else:
            winner = team2["name"]
        '''

        with open(f'export/gc_chunked_json/chunk{count}.txt', 'w', encoding="utf-8") as j:
            #j.write(f"""This game, of event {event} from the tournament {tour} was played between {team1["name"]} from {team1["country"]} and {team2["name"]} from {team2["country"]}, ended with {winner} being the winners of the match.\nThe score was {team1["name"]} with {team1["score"]} to {team2["name"]} with {team2["score"]}. The game was completed around the relative date of {relativeDate}.""")
            json.dump(i, j, ensure_ascii=False)
        j.close()

        count += 1
    
    return True

def chunkSepPt3():
    with open('game data/tournament/game_changers_data.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    f.close()

    teamMap = {}

    dupCheck = []

    for i in data:
        
        if i in dupCheck:
            continue

        dupCheck.append(i)

        teams = i["teams"]

        team1 = teams[0]
        team2 = teams[1]

        if(team1["name"] not in teamMap):
            teamMap[team1["name"]] = {"name":team1["name"], "country":team1["country"]} #init
        if(team2["name"] not in teamMap):
            teamMap[team2["name"]] = {"name":team2["name"], "country":team2["country"]} #init
        
        ptr = teamMap[team1["name"]]
        ptr2 = teamMap[team2["name"]]

        if "wins" not in ptr:
            ptr["wins"] = 0
            ptr["loses"] = 0
        if "wins" not in ptr2:
            ptr2["wins"] = 0
            ptr2["loses"] = 0

        if(team1["won"]):
            ptr["wins"] += 1
        else:
            ptr["loses"] += 1
        
        if(team2["won"]):
            ptr2["wins"] += 1
        else:
            ptr2["loses"] += 1

    count = 1
    for i in teamMap:
        if(i == ":3" or i == "Kitten Gaming<3"):
            with open(f'export/gc_chunked_team_key/illegalname{count}.txt', 'w', encoding="utf-8") as j:
                json.dump(teamMap[i], j, ensure_ascii=False)
            count += 1
        else:
            with open(f'export/gc_chunked_team_key/{i}.txt', 'w', encoding="utf-8") as j:
                json.dump(teamMap[i], j, ensure_ascii=False)
        j.close
    
    return True

def playerChunk():
    with open('player_data_2023_2024.csv', 'r', encoding='utf-8') as f:
        data = list(csv.DictReader(f, delimiter=","))
    f.close()

    for i in data:
        playerName = i["Player"].split("\n", 1)[0] #grab only player name

        i['Player'] = playerName

        with open(f'export/players_chunked/{playerName}.txt', 'w', encoding="utf-8") as j:
            json.dump(i, j, ensure_ascii=False)
    
    return True