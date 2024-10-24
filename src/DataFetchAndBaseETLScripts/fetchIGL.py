from bs4 import BeautifulSoup
import requests
import json

class Player:
    def __init__(self,name, team, y_active):
        self.name = name
        self.team = team
        self.years_active = y_active

def my_converter(obj):
    if isinstance(obj, Player):
        return obj.__dict__  # Convert object to dictionary
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


igl_url = 'https://liquipedia.net/valorant/Category:In-game_leaders'
igl_url_page2 = 'https://liquipedia.net/valorant/index.php?title=Category:In-game_leaders&pagefrom=Syfi#mw-pages'

base_url = "https://liquipedia.net"

page1 = requests.get(igl_url)
soup = BeautifulSoup(page1.content, 'html.parser')


page2 = requests.get(igl_url_page2)
soup2 = BeautifulSoup(page2.content, 'html.parser')


columns = soup.find_all('div', class_='mw-category-group')
columns_2nd_page = soup2.find_all('div', class_='mw-category-group')


player_page_endpoints =[]
for player in columns:
    for title in player.find_all('a', href=True):
        player_page_endpoints.append(title['href'])

for player in columns_2nd_page:
    for title in player.find_all('a', href=True):
        player_page_endpoints.append(title['href'])



player_info_list = []




for end_point in player_page_endpoints:
    try:


        player_page = requests.get(base_url+end_point)

        player_soup = BeautifulSoup(player_page.content, 'html.parser')

        player_keys= player_soup.find_all('div', attrs= {'class':'infobox-cell-2 infobox-description'})

        player_values = player_soup.find_all('div', attrs= {'style':'width:50%'})

        team_index =0 

        years_active_index = 0




        for a in player_keys:
            if a.get_text() == 'Team:' :
                team_index = player_keys.index(a)
        

            if a.get_text()== 'Years Active (Player):':
                years_active_index = player_keys.index(a)       


        player_info_list.append(Player(end_point.split('/')[-1], player_values[team_index].get_text() if team_index !=0 else None, player_values[years_active_index].get_text() if years_active_index != 0 else None))
        
    except:
        print("exception in endpoint: " + end_point)

    print('Done :', player_page_endpoints.index(end_point))



json_str = json.dumps(player_info_list, default=my_converter)

# Save to a JSON file
with open('igls.json', 'w') as json_file:
    json_file.write(json_str)

print(json_str)