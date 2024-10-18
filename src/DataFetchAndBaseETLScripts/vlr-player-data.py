import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os


def scrape_event_data(event_name, event_id):
    url = f'https://www.vlr.gg/stats/?event_group_id={event_id}&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all'
    print(f'Scraping data from: {url}')
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', class_='wf-table mod-stats mod-scroll')
    if table is None:
        print(f"No table found for {event_name}. Check the page structure or event ID.")
        return None  
    
    headers = [th.text.strip() for th in table.find_all('th')]
    headers.append('Player URL') 
    
    rows = []
    for row in table.find_all('tr')[1:]: 
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]

        player_link = row.find('a', href=True) 
        if player_link:
            player_url = 'https://www.vlr.gg' + player_link['href'] + '?timespan=all'
            player_name = player_link.text.strip()  
            player_name = player_name.replace('\n', '').strip()
        else:
            player_url = 'N/A'
            player_name = 'N/A'
        
        row_data.append(player_url) 
        
      
        rows.append(row_data)

    for r in rows:
        if len(r) != len(headers):
            print(f'Warning: Row length {len(r)} does not match header length {len(headers)}.')

    df = pd.DataFrame(rows, columns=headers)
    
    if 'Agent' in df.columns:
        df.drop(columns=['Agent'], inplace=True)
    
    if 'Player' in df.columns:  
        df.drop(columns=['Player'], inplace=True)



    column_mapping = {
        'Player': 'Player',
        'Agents': 'Agents',
        'Rnd': 'Rounds Played',
        'R2.0': 'Rating',
        'ACS': 'Average Combat Score',
        'K:D': 'Kills:Death',
        'KAST': 'Kill, Assist, Survive, Trade Percent',
        'ADR': 'Average Damage per Round',
        'KPR': 'Kills Per Round',
        'APR': 'Assists Per Round',
        'FKPR': 'First Kills Per Round',
        'FDPR': 'First Deaths Per Round',
        'HS%': 'Headshot Percent',
        'CL%': 'Clutch Success Percent',
        'CL': 'Clutches (won/played)',
        'KMax': 'Maximum Kills in a single map',
        'K': 'Kills',
        'D': 'Deaths',
        'A': 'Assists',
        'FK': 'First Kills',
        'FD': 'First Deaths',
        'Player URL': 'Player URL'
    }

    df.rename(columns=column_mapping, inplace=True)

    return df 

events = {
    'Valorant Game Changers 2023': '38',
    'Valorant Game Changers 2024': '62',
    'Challengers League 2023': '31',
    'Challengers League 2024': '59',
    'Valorant Champions Tour 2023': '45',
    'Valorant Champions Tour 2024': '61'
}

all_dataframes = {} 

for event_name, event_id in events.items():
    event_df = scrape_event_data(event_name, event_id) 
    if event_df is not None: 
        all_dataframes[event_name] = event_df

def scrape_player_profiles(url, output_folder, player_stats ):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='wf-table')
 
    # Initialize lists to store the data
    agent_data = []
    headers = []
    player_data = []

    for th in table.find_all('th'):
        title = th.get('title')
        if title:  
            headers.append(title)

    for row in table.find_all('tr')[1:]:  
        cols = row.find_all('td')
        if cols: 
            row_data = {}
            for i, col in enumerate(cols):
                if headers[i] == "Agent":  
                    img = col.find('img')
                    if img: 
                        row_data[headers[i]] = img.get('alt', 'Unknown')
                    else:
                        row_data[headers[i]] = 'Unknown'  
                else:
                    text = col.get_text(strip=True)
                    row_data[headers[i]] = text

            agent_data.append(row_data)

    current_team_section = None
    for header in soup.find_all('h2', class_='wf-label mod-large'):
        header_text = header.get_text(strip=True)

        if header_text == "Current Teams":
            current_team_section = header.find_next('div', class_='wf-card')
            break  

    team_name = "Unknown"

    if current_team_section:
        team_name_div = current_team_section.find('div', {'style': 'font-weight: 500;'})

        if team_name_div:
            team_name = team_name_div.get_text(strip=True)
            #print(f"{team_name}")




    player_id = url.split('/')[4] 
    player_name = url.split('/')[5]  
    player_name = player_name.split('?')[0] 
    player_name = player_name.replace('/', '') 
    #print(player_name)
    
    df = pd.DataFrame(agent_data)
    df['Rounds by Agents'] = df['Usage'].str.extract(r'\((\d+)\)')[0].astype(int)  
    df['Usage'] = df['Usage'].str.replace(r'\(\d+\)\s*', '', regex=True)  
    df['Usage'] = df['Usage'].str.replace('%', '', regex=True).astype(float)  

    df = df[df['Usage'] >= 5]  
    Total_Games = int(df['Rounds by Agents'].astype(int).sum())
    first_5_agents = df['Agent'].head(5).tolist() if not df.empty else []
    df_to_save = df.to_dict(orient='records')    
    
    stats = {
        "Rounds Played": player_stats.get('Rounds Played', None),
        "Rating": player_stats.get('Rating', None),
        "Average Combat Score": player_stats.get('Average Combat Score', None),
        "Kills:Death": player_stats.get('Kills:Death', None),
        "Kill, Assist, Survive, Trade Percent": player_stats.get('Kill, Assist, Survive, Trade Percent', None),
        "Average Damage per Round": player_stats.get('Average Damage per Round', None),
        "Kills Per Round": player_stats.get('Kills Per Round', None),
        "Assists Per Round": player_stats.get('Assists Per Round', None),
        "First Kills Per Round": player_stats.get('First Kills Per Round', None),
        "First Deaths Per Round": player_stats.get('First Deaths Per Round', None),
        "Headshot Percent": player_stats.get('Headshot Percent', None),
        "Clutch Success Percent%": player_stats.get('Clutch Success Percent', None),
        "Clutches (won/played)": player_stats.get('CL', None),
        "Maximum Kills in a single map": player_stats.get('Maximum Kills in a single map', None),
        "Kills": player_stats.get('Kills', None),
        "Deaths": player_stats.get('Deaths', None),
        "Assists": player_stats.get('Assists', None),
        "First Kills": player_stats.get('First Kills', None),
        "First Deaths": player_stats.get('First Deaths', None),
    }

    
    json_output = {
        "Player URL": url,
        "All Agents Stats": df.to_dict(orient='records'),
        "Current Team": team_name,
        "Player": player_name,
        "Signature Agents Ranked by Usage": first_5_agents,
        "Total games played": Total_Games,
        "Player stats": stats
    }
    
    os.makedirs(output_folder, exist_ok=True)

    json_filename = os.path.join(output_folder, f"{player_name.replace(' ', '_')}_{player_id}_profile.json")
    
    try:
        with open(json_filename, 'w') as json_file:
            json.dump(json_output, json_file, indent=4)
        #print(f"Data has been successfully saved to {json_filename}")
    except Exception as e:
        print(f"Error saving JSON: {e}")

def scrape_profiles_from_cleaned_data(df, output_folder):
    for index, player_row in df.iterrows():
        player_url = player_row.iloc[-1] 
        if pd.notna(player_url): 
            player_stats = {
                "Rounds Played": player_row['Rounds Played'],
                "Rating": player_row['Rating'],
                "Average Combat Score": player_row['Average Combat Score'],
                "Kills:Death": player_row['Kills:Death'],
                "Kill, Assist, Survive, Trade Percent": player_row['Kill, Assist, Survive, Trade Percent'],
                "Average Damage per Round": player_row['Average Damage per Round'],
                "Kills Per Round": player_row['Kills Per Round'],
                "Assists Per Round": player_row['Assists Per Round'],
                "First Kills Per Round": player_row['First Kills Per Round'],
                "First Deaths Per Round": player_row['First Deaths Per Round'],
                "Headshot Percent": player_row['Headshot Percent'],
                "Clutch Success Percent": player_row['Clutch Success Percent'],
                "Clutches (won/played)": player_row['Clutches (won/played)'],
                "Kills Max": player_row['Maximum Kills in a single map'],
                "Kills": player_row['Kills'],
                "Deaths": player_row['Deaths'],
                "Assists": player_row['Assists'],
                "First Kills": player_row['First Kills'],
                "First Deaths": player_row['First Deaths'],
            }
            scrape_player_profiles(player_url, output_folder, player_stats) 

output_folder = 'player_profiles'  # Base output folder

for event_name, df in all_dataframes.items():          
    event_output_folder = os.path.join(output_folder, event_name.replace(' ', '_'))  
    os.makedirs(event_output_folder, exist_ok=True) 
    scrape_profiles_from_cleaned_data(df, event_output_folder)




