import json

with open("game data/tournament/game_changers_data.json", "r", encoding="utf8") as f:
    gcdata = json.load(f)

count = 0

for i in gcdata:
    for j in i["teams"]:
        if(j["name"] == "BBL Queens" and j["won"] == True):
            count += 1

print(count)