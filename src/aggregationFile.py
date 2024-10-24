#Aggregation File
import os
import json
import pandas as pd
import numpy as np
import csv

#players_chunked
def aggregation(folder_name): #type is folder name
    directory = f"C:/Users/handy/Desktop/Codebase/VCT-Hackathon/src/export/{folder_name}/"

    df = pd.DataFrame(columns=["Player", "Team", "Games", "SignatureAgentsRankedByUsage", "RoundsPlayed", "Rating", "AverageCombatScore", "KillsDeath", "KAST", "ADPR", "KPR", "APR", "FKPR", "FDPR", "HeadshotPercent", "ClutchSuccessPercent", "Kills", "Deaths", "Assists", "FirstKills", "FirstDeaths", "Year", "League", "IGL", "CleanedRating", "AdjustedRating", "SelflessIndex"])
    #df2 is overall player and agent database, super large file and data
    df2 = pd.DataFrame(columns=["Player", "Team", "Agent", "Usage", "RoundsPlayed", "Rating", "AverageCombatScore", "KillsDeath", "ADPR", "KAST", "KPR", "APR", "FKPR", "FDPR", "Kills", "Deaths", "Assists", "FirstBloods", "FirstDeaths", "Games", "CleanedRating", "AdjustedRating", "SelflessIndex"])
    counter = 0

    with open("helper/igls.json", 'r', encoding="utf8") as igl:
        igldata = json.load(igl)
    iglArr = []
    for i in igldata['In Game Leads']:
        iglArr.append(i['name'].lower())

    with open('helper/regionMap.json', 'r', encoding='utf-8') as region:
        regionMap = json.load(region)

    for folder in os.listdir(directory):
        for name in os.listdir(directory + folder + "/"):
            row = [] #var for df
            with open(directory + "/" + folder + "/" + name, 'r', encoding='utf-8') as f:
                if not f:
                    break
                if('.csv' in name):
                    print("csv found, skipping to next.")
                    continue #move to next file
                data = json.load(f)
            if(folder_name == 'players_chunked'):
                toParse = data['Player stats']
                agentData = data['All Agents Stats']
            print('working on ' + data['Player'])
            row.append(data['Player'])
            row.append(data['Current Team'])
            row.append(data["Total games played"])
            row.append(data['Signature Agents Ranked by Usage'])
            row.append(toParse['Rounds Played'])
            row.append(toParse['Rating'])
            row.append(toParse['Average Combat Score'])
            row.append(toParse['Kills:Death'])
            row.append(toParse['Kill, Assist, Survive, Trade Percent'])
            row.append(toParse['Average Damage per Round'])
            row.append(toParse['Kills Per Round'])
            row.append(toParse["Assists Per Round"])
            row.append(toParse["First Kills Per Round"])
            row.append(toParse["First Deaths Per Round"])
            row.append(toParse["Headshot Percent"])
            row.append(toParse["Clutch Success Percent%"])
            row.append(toParse["Kills"])
            row.append(toParse["Deaths"])
            row.append(toParse["Assists"])
            row.append(toParse["First Kills"])
            row.append(toParse["First Deaths"])
            row.append(folder[-4:])
            row.append(folder[:-5])
            if(data['Player'].lower() in iglArr): #IGL Flag
                row.append(True)
            else:
                row.append(False)
            row.append(toParse["Rating"])
            row.append(np.nan)
            row.append(np.nan)
            df.loc[len(df)+1] = row
            for i in agentData:
                row2 = []
                row2.append(data['Player'])
                row2.append(data['Current Team'])
                row2 += list(i.values())
                row2 += [np.nan] * 3
                df2.loc[len(df2)+1] = row2
        #if(counter == 1): #skips every other iterations, combines years data
    df = df.replace('', np.nan)
    df['Rating'] = pd.to_numeric(df["Rating"], errors='coerce')
    df['CleanedRating'] = df['CleanedRating'].fillna(df.groupby('Year')['Rating'].transform('mean'))
    df['RoundsPlayed'] = pd.to_numeric(df['RoundsPlayed'], errors='coerce')
    df['CleanedRating'] = pd.to_numeric(df['CleanedRating'], errors='coerce')
    df['AdjustedRating'] = (
        (np.log(df['RoundsPlayed'].astype(int))) / 
        (np.log(df['RoundsPlayed'].astype(int).max()))) * df["CleanedRating"]
    df['KPR'] = pd.to_numeric(df['KPR'], errors='coerce')
    df['APR'] = pd.to_numeric(df['APR'], errors='coerce')
    df['SelflessIndex'] = (df['APR'] / df['KPR'])
    df = df.round(2)
    df.to_csv("export/toSQL/player.csv", index=False)
    print("Completed player.csv")
            #counter = 0
        #else:
        #    counter += 1
    df2 = df2.replace('', np.nan)
    df2 = df2.drop_duplicates()
    df2['CleanedRating'] = df2['Rating']
    df2['Rating'] = pd.to_numeric(df2["Rating"], errors='coerce')
    df2['CleanedRating'] = df2['CleanedRating'].fillna(df2['Rating'].mean(skipna=True))
    df2['RoundsPlayed'] = pd.to_numeric(df2['RoundsPlayed'], errors='coerce')
    df2['CleanedRating'] = pd.to_numeric(df2['CleanedRating'], errors='coerce')
    df2['AdjustedRating'] = ((np.log(df2['RoundsPlayed'].astype(int))) / (np.log(df2['RoundsPlayed'].astype(int).max()))) * df2['CleanedRating']
    df2['KPR'] = pd.to_numeric(df2['KPR'], errors='coerce')
    df2['APR'] = pd.to_numeric(df2['APR'], errors='coerce')
    df2['SelflessIndex'] = df2['APR'] / df2['KPR']
    df2 = df2.round(2)
    df2 = df2.loc[df2['Usage'] > 10]
    df2.to_csv("export/toSQL/player_agent_performance.csv", index=False)
    print("completed full run and aggregation of players and agent data")   

def aggregateTeams():
    df1 = pd.DataFrame(columns=['TeamId', 'Name', 'Country', 'Wins', 'Loses', 'Winrate', 'GameChangerWins', 'GameChangerLoses', 'Region', 'Status'])
    df2 = pd.DataFrame(columns=['TeamId', 'Player', 'RoleStatus'])

    with open(f'helper/regionMap.json', 'r', encoding='utf8') as j:
        jData = json.load(j)

    for name in os.listdir("C:/Users/handy/Desktop/Codebase/VCT-Hackathon/src/export/team_key_chunked/"):
        with open(f"export/team_key_chunked/{name}", 'r', encoding='utf8') as f:
            if not f:
                continue
            data = json.load(f)
        print(f"aggregating and appending {data['name']}")
        row = []
        row += list(data.values())[:8]

        for i in jData: 
            if(data['region'] in jData[i] or data['country'] in jData[i]):
                row.append(i)
                break
        if(len(row) != 9):
            row.append('N/A')
        row.append(data['status'])
        df1.loc[len(df1)+1] = row #team df 

        for i in data['players']:
            row2 = []
            row2.append(data['id'])
            valueSet = list(i.values())
            valueSet.pop(1)
            row2 += valueSet
            df2.loc[len(df2)+1] = row2
    
    df1 = df1.replace('', np.nan)
    df1.to_csv("export/toSQL/team_data.csv", index=False)

    df2 = df2.replace('', np.nan)
    df2.to_csv("export/toSQL/player_team_map.csv", index=False)

    return True
        
def joinRegions():
    files = ["player.csv"]

    team_data_df = pd.read_csv('export/toSQL/team_data.csv')

    for i in files:
        data = pd.read_csv(f'export/toSQL/{i}')

        data = data.merge(team_data_df[['Name','Region']], left_on='Team', right_on='Name')
        data = data.drop(columns=['Name'])
        
        data.to_csv(f'export/toSQL/{i}', index=False)
    
    return 
        



