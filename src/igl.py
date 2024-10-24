import json
import pandas as pd

def iglCleanAndSQL():
    with open("igls.json", 'r', encoding="utf8") as f:
        data = json.load(f)
    df = pd.DataFrame(columns=["Player", "Team", "Years_Active", "Active", "YearsOfExperience"])
    for i in data['In Game Leads']:
        row = []
        toParse = i['years_active']
        if(toParse == None):
            continue
        splitValues = toParse.split(" ")
        if(splitValues[-1] == "Present"):
            i['active'] = True
            i['yearsOfExperience'] = 2024 - int(splitValues[0])
        else:
            i['active'] = False
            i['yearsOfExperience'] = int(splitValues[-1]) - int(splitValues[0])
        row = list(i.values())
        df.loc[len(df)+1] = row
    df.to_csv("export/iglData/igl.csv", index=False)
    return