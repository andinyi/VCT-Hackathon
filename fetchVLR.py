import requests
import json
import os

url = "https://vlr.orlandomm.net/api/v1/results?page="

i = 0

while(True):

    pageFetch = url + str(i)

    response = requests.get(pageFetch)

    if(response.status_code == 200 and i <= 527):
        
        if not os.path.isfile("dataCleaned.json"):
            with open('dataCleaned.json', 'w', encoding='utf-8') as f:
                json.dump(response.json().get("data"), f, ensure_ascii=False)
        else:
            with open('dataCleaned.json', 'a', encoding='utf-8') as f:
                json.dump(response.json().get("data"), f, ensure_ascii=False)

        print(f"wrote page {i} and saved data into data file")
    
    else:
        break

    i += 1

print("completed result fetch run")   