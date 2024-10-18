from datetime import datetime
from dateutil.relativedelta import relativedelta

def recalcDT(val):
    
    year = 0
    month = 0
    week = 0
    day = 0
    hour = 0

    if 'y' in val:
        year = int(val[val.find('y') - 1])
    if 'mo' in val:
        if(val[val.find('mo') - 1].isnumeric() and val[val.find('mo') - 2].isnumeric()):
            month = int(val[val.find('mo') - 2] + val[val.find('mo') - 1])
        else:
            month = int(val[val.find('mo') - 1])
    if 'w' in val:
        if(val[val.find('w') - 1].isnumeric() and val[val.find('w') - 2].isnumeric()):
            week = int(val[val.find('w') - 2] + val[val.find('w') - 1])
        else:
            week = int(val[val.find('w') - 1])
    if 'd' in val:
        if(val[val.find('d') - 1].isnumeric() and val[val.find('d') - 2].isnumeric()):
            day = int(val[val.find('d') - 2] + val[val.find('d') - 1])
        else:
            day = int(val[val.find('d') - 1])
    if 'h' in val:
        if(val[val.find('h') - 1].isnumeric() and val[val.find('h') - 2].isnumeric()):
            hour = int(val[val.find('h') - 2] + val[val.find('h') - 1])
        else:
            hour = int(val[val.find('h') - 1])
    
    place = datetime(2024, 9, 16, 23, 59, 00) #time of data pull

    return place - relativedelta(years=year, months=month, weeks=week, days=day, hours=hour)

def rowParse(input):
    rows = []

    for row in input:
        rowData = []
        tdList = row.find_all("td")
        for td in tdList:
            #print(td['class'])
            if(td.get('class')[0] == "mod-player"): 
                rowData.append(td.find("div", class_="text-of").text.strip())
            elif(td.get('class')[0] == "mod-agents"):
                agents = td.find_all("img")
                agentList = []
                for agent in agents:
                    agentList.append(agent['title'])
                rowData.append(agentList)
            elif(td.get('class')[-1] == "mod-fk-diff" or td.get('class')[-1] == "mod-kd-diff"):
                stats = td.find("span", class_="stats-sq").find_all("span", "side")
                btct = {} #both t and ct scores
                for stat in stats:
                    btct[stat["class"][1]] = stat.text.strip()
                formatString = f"{btct['mod-t'] if 'mod-t' in btct else "NA"} on Attacker Side |{btct['mod-ct'] if 'mod-ct' in btct else "NA"} on Defender Side | {btct['mod-both'] if 'mod-both' in btct else "NA"} Overall."
                rowData.append(formatString)
            else:
                stats = td.find("span", class_="stats-sq").find_all("span", "side")
                btct = {} #both t and ct scores
                for stat in stats:
                    btct[stat["class"][-1]] = stat.text.strip()
                formatString = f"{btct['mod-t'] if 'mod-t' in btct else "NA"} on Attacker Side |{btct['mod-ct'] if 'mod-ct' in btct else "NA"} on Defender Side | {btct['mod-both'] if 'mod-both' in btct else "NA"} Overall."
                rowData.append(formatString)

        rows.append(rowData)
    
    return rows