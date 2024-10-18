import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import json

#import utils

'''
# Function to scrape data for a specific event
def scrape_event_data(event_name, event_id):
    url = f'https://www.vlr.gg/stats/?event_group_id={event_id}&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all'
    print(url)
    
    # Send an HTTP request to the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table with player stats
    table = soup.find('table')
    if table is None:
        print(f"No table found for {event_name}. Check the page structure or event ID.")
        return None  # Return None if no table is found
    
    # Extract the table headers
    headers = [th.text for th in table.find_all('th')]
    headers.append('Agent Image URLs')  # Add a column for agent image URLs
    headers.append('Player URL')  # Add a column for player URLs
    
    # Extract table rows
    rows = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        
        # Find the 'mod-agents' column that contains multiple images
        agent_td = row.find('td', class_='mod-agents')
        if agent_td:
            agent_imgs = agent_td.find_all('img')
            img_urls = [img['src'].replace('/img/vlr/game/agents/', '').replace('.png', '') for img in agent_imgs] if agent_imgs else ['N/A']
        else:
            img_urls = ['N/A']
        
        row_data.append(', '.join(img_urls))  # Append the list of image URLs to the row
        
        # Find the player's profile link
        player_link = row.find('a')
        if player_link and 'href' in player_link.attrs:
            player_url = 'https://www.vlr.gg' + player_link['href']+ '?timespan=all'
        else:
            player_url = 'N/A'
        
        
        row_data.append(player_url)  # Append the player URL to the row
        rows.append(row_data)
    
    # Convert the data into a DataFrame
    df = pd.DataFrame(rows, columns=headers)
    #print(df)
    
    return df  # Return the DataFrame

# List of events with correct event IDs
events = {
    'Valorant Game Changers 2023': '38',
    'Valorant Game Changers 2024': '62',
    'Challengers League 2023': '31',
    'Challengers League 2024': '59',
    'Valorant Champions Tour 2023': '45',
    'Valorant Champions Tour 2024': '61'
}

# List to hold DataFrames
all_dataframes = []

# Loop through each event and scrape data
for event_name, event_id in events.items():
    event_df = scrape_event_data(event_name, event_id)
    if event_df is not None:
        all_dataframes.append(event_df)  # Add the DataFrame to the list

# Concatenate all DataFrames and save as a single CSV
if all_dataframes:
    final_df = pd.concat(all_dataframes, ignore_index=True)
    final_df.to_csv('all_events_data.csv', index=False)
    print("All event data saved as all_events_data.csv")



# Replace 'Player Name' with the actual column name for player names in your dataset

final_df = final_df.drop_duplicates(subset=['Player'], keep='first')

# Save the cleaned DataFrame to a new CSV file
final_df.to_csv('cleaned_player_data.csv', index=False)

print("Duplicates removed and saved to cleaned_player_data.csv")

'''

# Function to scrape player profiles for agents and team name
def scrape_player_profiles(player_df):
    # Create a DataFrame to hold agent data for all players
    all_agent_data = []

    # Iterate through each player's URL in the DataFrame
    for index, row in player_df.iterrows():
        player_url = row['Player URL']
        print(f"Fetching data for player: {player_url}")

        # Initialize retry variables
        retries = 3
        for attempt in range(retries):
            try:
                # Fetch the player's profile page
                player_response = requests.get(player_url)
                player_response.raise_for_status()  # Check for HTTP errors
                player_soup = BeautifulSoup(player_response.text, 'html.parser')

                # Extract agent data
                agent_table = player_soup.find('table', {'class': 'wf-table'})  # Use class to identify the table
                agent_data_list = []  # Temporary list to store agent data for the current player
                
                if agent_table:
                    print("Agent Table Found. Extracting agent names and images...")
                    agent_rows = agent_table.find_all('tr')[1:]  # Skip header
                    if not agent_rows:
                        print("No agent rows found in the table.")
                    for agent_row in agent_rows:
                        # Find agent image and name
                        agent_img_tag = agent_row.find('img')
                        agent_img_url = 'https://www.vlr.gg' + agent_img_tag['src'] if agent_img_tag else 'N/A'
                        
                        agent_name = agent_row.find('td', style="padding-left: 8px; padding-right: 8px;").text.strip() if agent_row.find('td', style="padding-left: 8px; padding-right: 8px;") else 'N/A'

                        agent_data_list.append({'Agent Name': agent_name, 'Image URL': agent_img_url})

                else:
                    print("No agent table found.")

                # Extract current team data
                team_section = player_soup.find('a', {'class': 'wf-module-item mod-first'})
                if team_section:
                    team_name = team_section.find('div', style="font-weight: 500;").text.strip()
                else:
                    team_name = 'N/A'

                # Store player URL and team name in all_agent_data list
                all_agent_data.append({'Player URL': player_url, 'All Agents': agent_data_list, 'Current Team': team_name})

                # Wait a bit between requests
                time.sleep(1)  # Adjust the delay as needed
                break  # Exit retry loop if successful

            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    print(f"Giving up on {player_url}")
                else:
                    time.sleep(2)  # Wait a bit before retrying

    # Create a DataFrame for all agent data
    agents_df = pd.DataFrame(all_agent_data)

    # Print the entire DataFrame
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.width', None)  # No limit on width

    print(agents_df)

    # Save the agent data DataFrame to CSV
    agents_df.to_csv('all_players_agents_data.csv', index=False)
    print("Agent data saved as all_players_agents_data.csv")

# Assuming the final DataFrame from the previous scraping step is named final_df
# You should replace this with the DataFrame you created earlier
# Scrape player profiles based on the DataFrame
#scrape_player_profiles(final_df)

#----------------------------------------------------------------------------------------------------------------------
#Scrapes Match Data, given a match id input
#Return is None, writes items to a folder with the match ids scraped
def scrape_match_vlr(match_id):

    multiGameCheck = False

    url = f"https://www.vlr.gg/{match_id}"
    response = requests.get(url)

    matchDetails = {}

    matchDetails["id"] = match_id

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    matchheader = soup.find("a", class_="match-header-event")
    matchheaderTitle = matchheader.find("div").find("div").text.strip()
    matchheaderEvent = matchheader.find("div").find("div", class_="match-header-event-series").text.strip().replace("\n", "").replace("\t", "")

    matchDetails["Tournament Name"] = matchheaderTitle
    matchDetails["Event Series"] = matchheaderEvent

    timeslotDiv = soup.find('div', {'data-utc-ts':True})

    if timeslotDiv:
        timeslot = timeslotDiv["data-utc-ts"]
        timeslot = datetime.datetime.strptime(timeslot, "%Y-%m-%d %H:%M:%S")
        matchDetails["date"] = str(timeslot.date())

    games = soup.find('div', class_='vm-stats-gamesnav-item')

    eventScore = soup.find('div', class_="js-spoiler").text.strip().replace("\n", "").replace("\t", "")
    matchDetails['eventScore'] = eventScore

    if(games):
        multiGameCheck = True
        team1_name = soup.find_all('div', class_='wf-title-med')[0].text.strip()
        team2_name = soup.find_all('div', class_='wf-title-med')[1].text.strip()
        pass
    else:
        multiGameCheck = False
        statbar = soup.find('div', class_="vm-stats-game-header")
        middlePart = statbar.find("div", class_="map")
        map = middlePart.find("span").text.strip()
        gameDuration = middlePart.find("div", class_="map-duration ge-text-light").text.strip()
        matchDetails["map"] = map
        matchDetails["gameDuration"] = gameDuration

        team1 = statbar.find('div', class_="team")
        team1_name = team1.find('div', class_='team-name').text.strip()
        team1_score = team1.find('div', class_='score').text.strip()
        team1_attack_score = team1.find("span", class_="mod-t").text.strip()
        team1_defense_score = team1.find("span", class_="mod-ct").text.strip()

        team2 = statbar.find('div', class_="team mod-right")
        team2_name = team2.find('div', class_='team-name').text.strip()
        team2_score = team2.find('div', class_='score').text.strip()
        team2_attack_score = team2.find("span", class_="mod-t").text.strip()
        team2_defense_score = team2.find("span", class_="mod-ct").text.strip()

    if(not multiGameCheck):
        tables = soup.find_all("table", class_="wf-table-inset")
        if(tables == None):
            print("No tabular data found, api call failed. Returning")
            return None
    else:
        tempHold = soup.find('div', class_='vm-stats-game mod-active')
        if(tempHold == None):
            print("No tabular data found, api call failed. Returning")
            return None
        tables = tempHold.find_all("table", class_="wf-table-inset")
    #table[0] grabs first team
    headersGrab = tables[0].find("tr")
    team1table = tables[0].find("tbody").find_all("tr")
    headers = [th.get('title', 'Player') for th in headersGrab.find_all('th')]
    rows1 = utils.rowParse(team1table)
    df1 = pd.DataFrame(rows1, columns=headers)
    df1 = df1.iloc[:,:-1]
    team1Convert = json.loads(df1.to_json(orient='records'))
    playerCount = 1
    team1Dict = {} #to be used for populating matchDetails
    team1SampleDict = {} #used to nest dictionary
    team1Dict['name'] = team1_name
    if(not multiGameCheck):
        team1Dict["scores"] = {"Total Score" : team1_score, "Attacker Side Score" : team1_attack_score, "Defender Side Score" : team1_defense_score}
    team1Dict["players"] = team1SampleDict
    for i in team1Convert:
        team1SampleDict[f'player{playerCount}'] = i
        playerCount += 1
    matchDetails["team1"] = team1Dict
    del team1Dict
    #####################################################################################################
    team2table = tables[1].find("tbody").find_all("tr")
    rows2 = utils.rowParse(team2table)
    df2 = pd.DataFrame(rows2, columns=headers)
    df2 = df2.iloc[:,:-1]
    team2Convert = json.loads(df2.to_json(orient="records"))
    playerCount = 1
    team2Dict = {}
    team2SampleDict = {}
    team2Dict['name'] = team2_name
    if(not multiGameCheck):
        team2Dict["scores"] = {"Total Score" : team2_score, "Attacker Side Score" : team2_attack_score, "Defender Side Score" : team2_defense_score}
    team2Dict["players"] = team2SampleDict
    for i in team2Convert:
        #add players to players field of team2Dict via adding them as separate entities in team2SampleDict
        team2SampleDict[f'player{playerCount}'] = i
        playerCount += 1
    matchDetails["team2"] = team2Dict
    del team2Dict

    if(int(eventScore[0]) > int(eventScore[-1])):
        matchDetails['winner'] = team1_name
    elif(int(eventScore[-1]) > int(eventScore[0])):
        matchDetails['winner'] = team2_name
    else:
        matchDetails['winner'] = "DRAW"
    
    with open(f"export/match_id_scraped_chunked/{match_id}.txt", "w", encoding="utf-8") as f:
        json.dump(matchDetails, f, ensure_ascii=False)
    #print(matchDetails)

#Pulls Team Ids Given a Match
#Returns an array of team ids, team1 vs team2.
def pullTeamIds(match_id):
    print(f"pulling for match {match_id}")
    url = f"https://www.vlr.gg/{match_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    matchup = soup.find("div", class_="wf-module-item match-h2h-header mod-first")
    teams = matchup.find_all("a")
    outputArr = []
    for team in teams:
        stringToBeParsed = team['href'] 
        parsed = stringToBeParsed.split('/')[2]
        outputArr.append(int(parsed))
    return outputArr

#Follow up function to pull team information given a team id.
#Returns a file written with information regarding the team.
def pullTeamInfo(team_id):
    print(f"pulling for team {team_id}")
    gameChangerFlag = False
    statusFlag = True
    url = f"https://www.vlr.gg/team/{team_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    teamStatus = soup.find("span", class_='team-header-status')
    if(teamStatus and "inactive" in teamStatus.text.strip()):
        statusFlag = False
    teamName = soup.find('h1', class_='wf-title').text.strip()
    teamRegion = soup.find('div', class_='team-header-country').text.strip()
    players = soup.find("div", class_="team-summary-container-1").find("div", class_="wf-card").find_all('div', class_='team-roster-item')
     
    container = soup.find_all('div', class_='team-rating-info')

    regions = []

    if not container:
        return #empty page case

    for i in container:
        ratingText = i.find('div', class_='rating-txt')
        if(ratingText):
            regions.append(ratingText.text.strip())
        if(ratingText and ratingText.text.strip() == "Game Changers"):
            gameChangerFlag = True
            gameChangerWins = i.find('span', 'win').text.strip("W ")
            gameChangerLoses = i.find('span', 'loss').text.strip("L ")
        w = i.find('span', 'win')
        l = i.find('span', 'loss')

    wins = w.text.strip("W ") if w else "N/A"
    loses = l.text.strip("L ") if l else "N/A"

    winrate = round(float(int(wins)/(int(loses) + int(wins))), 3) if w and l else "N/A"
    team = {}
    team['id'] = team_id
    team['name'] = teamName
    team['country'] = teamRegion
    team['wins'] = wins
    team['loses'] = loses
    team['winrate'] = winrate 
    if(gameChangerFlag):
        team['gameChangerWins'] = gameChangerWins
        team['gameChangerLoses'] = gameChangerLoses
    else:
        team['gameChangerWins'] = 'N/A'
        team['gameChangerLoses'] = 'N/A'
    if(len(regions) > 0):
        team['region'] = regions[0] if regions[0] != "Game Changers" else regions[1]
    else: 
        team['region'] = "N/A"
    team['status'] = "Active" if statusFlag else "Inactive"
    tempHolder = []
    for player in players:
        IGNname = player.find("div", "team-roster-item-name-alias").text.strip()
        IRLname = player.find("div", "team-roster-item-name-real")
        role = player.find("div", class_="wf-tag")
        dummy = {"playerName" : IGNname, "realName" : IRLname.text.strip() if IRLname else "N/A", 'role': role.text.strip() if role else 'player'}
        tempHolder.append(dummy)
    team['players'] = tempHolder

    with open(f"export/team_key_chunked/{team_id}.txt", "w", encoding="utf-8") as f:
        json.dump(team, f, ensure_ascii=False)

#scrape_match_vlr(361129)
#pullTeamInfo(1001)
#408103
#400866