import playerGrab
import json
import os 

#Simple Call for MatchPull with IDs referencing function in playerGrab
#scrape_match_vlr creates a json file with details of the match outputted to export/match_id_scraped_chunked

#Implementation Scrapped as we Switched to SQL Implemented.
def inDepthMatchPull(fileName):
    with open(f'game data/tournament/{fileName}', 'r', encoding="utf8") as f:
        data = json.load(f)
    for i in data:
        matchid = i['id']
        playerGrab.scrape_match_vlr(matchid)
    print(f"Completed Export of All MatchDetails for the File Match {fileName}")
    return True

#Grabs a list of team ids that played in each tournament. This data is then saved into a teamIds.json file that will be used to grab further team details.
def teamIdExport():
    export = [] #array to store all ids
    for file in os.listdir('C:/Users/handy/Desktop/Codebase/VCT-Hackathon/game data/tournament/'):
        print(f"Working on {file}")
        with open(f'game data/tournament/{file}', 'r', encoding="utf8") as f:
            data = json.load(f)
        for i in data:
            matchid = i['id']
            c = playerGrab.pullTeamIds(matchid) #pulls team ids for the match
            export.append(c[0])
            export.append(c[1])
    export = list(set(export)) #removes duplicates
    with open('helper/teamIds.json', 'w', encoding='utf8') as j:
        json.dump(export, j, ensure_ascii=False) #export json of teamIds

def teamPull(teamIDFile):
    with open(teamIDFile, 'r', encoding='utf8') as f:
        data = json.load(f)
    for i in data: #for each id
        playerGrab.pullTeamInfo(i)
    print('Completed Team Grab, Check Export Folder')

#inDepthMatchPull("game_changers_data.json")
#teamIdExport()
#teamPull("teamIds.json")