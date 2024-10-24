import json
import os

with open("game data/esports-data/game-changers-2024/mapping_data.json", "r", encoding="utf8") as mapping_f:
    mapping = json.load(mapping_f)
mapping_f.close()

with open("game data/esports-data/game-changers-2024/players.json", "r", encoding="utf8") as players_f:
    players = json.load(players_f)
players_f.close()

with open("game data/esports-data/game-changers-2024/teams.json", "r", encoding="utf8") as teams_f:
    teams = json.load(teams_f)
teams_f.close()

with open("game data/esports-data/game-changers-2024/tournaments.json", "r", encoding="utf8") as tournaments_f:
    tournaments = json.load(tournaments_f)
tournaments_f.close()

with open("game data/esports-data/game-changers-2024/leagues.json", "r", encoding="utf8") as leagues_f:
    leagues = json.load(leagues_f)
leagues_f.close()

leagueMap = {}
trMap = {}
teamMap = {}
playerMap = {}

for i in leagues:
    new_dict = {k: v for k, v in i.items() if k in {'league_id', 'name', 'region'}}
    leagueMap[i["league_id"]] = new_dict

for i in tournaments:
    new_dict = {k: v for k, v in i.items() if k in {'id', 'name'}}
    new_dict["league"] = leagueMap[i["league_id"]]
    trMap[i["id"]] = new_dict

for i in teams:
    new_dict = {k: v for k, v in i.items() if k in {'id', 'acronym','name'}}
    new_dict["league"] = leagueMap[i["home_league_id"]]
    teamMap[i["id"]] = new_dict

for i in players:
    new_dict = {k: v for k, v in i.items() if k in {'id', 'handle','first_name', 'last_name', 'status'}}
    if(i["home_team_id"] in teamMap):
        new_dict['home_team'] = teamMap[i["home_team_id"]]["name"]
    else:
        new_dict["home_team"] = i["home_team_id"]
    playerMap[i["id"]] = new_dict

for i in mapping:
    i["tournamentId"] = trMap[i["tournamentId"]]
    for j in i["teamMapping"]:
        if (i["teamMapping"][j] in teamMap):
            i["teamMapping"][j] = teamMap[i["teamMapping"][j]]
    for k in i["participantMapping"]:
        if (i["participantMapping"][k] != '-' and i["participantMapping"][k] in playerMap):
            i["participantMapping"][k] = playerMap[i["participantMapping"][k]]
        

with open("mappingJoinedGameChangers.json", "w", encoding="utf8") as out:
    json.dump(mapping, out, ensure_ascii=False)

print("Completed Mapping Write for file Game Changers.")








