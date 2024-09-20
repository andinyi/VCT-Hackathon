import json
import os
import datetime

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
