import requests
from dotenv import load_dotenv
import os 

load_dotenv()


url = "https://v3.football.api-sports.io/standings"
headers = {
    "x-apisports-key": os.getenv("API_KEY")
}

params = {
    "league": 39,
    "season": 2024
}

response = requests.get(url, headers=headers, params=params)
print(response.json())
#create json file 
with open("standings.json", "w") as f:
    f.write(response.text)

