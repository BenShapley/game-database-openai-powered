import json
import requests

with open("keys/rawg_keys.json", "r") as rawg_files:
    rawg_keys = json.load(rawg_files)

rawg_key = rawg_keys["client_key"]
to_search = f"Call%20of%20Duty:%20Black%20Ops"

def game_id_grabber():
    url = f"https://api.rawg.io/api/games?key={rawg_key}&search={to_search}"
    response = requests.get(url)
    data = response.json()
    print(data["results"][0]["id"])

game_id_grabber()