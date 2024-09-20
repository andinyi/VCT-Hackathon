import json
import datetime
import utils

lineMap = dict()

with open('dataCleaned.json', 'r', encoding="utf-8") as f:
    read = json.load(f)

for i in read:
    tmp = i['ago']
    i['ago'] = str(utils.recalcDT(tmp).date())

with open('dataCleaned.json', 'w', encoding="utf-8") as j:
    json.dump(read, j, ensure_ascii=False)

#with open('dataCleaned.json', 'w', encoding='utf-8') as o:
#    o.writelines(readLines)
    
