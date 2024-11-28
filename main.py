import json
import requests

with open("keys/rawg_keys.json", "r") as rawg_files:
    rawg_keys = json.load(rawg_files)

rawg_key = rawg_keys["client_key"]
to_search = f"Call%20of%20Duty:%20Black%20Ops"

test_input = input("Enter a game name:")
modified_string = test_input.replace(" ", "%20")

def game_id_grabber():
    url = f"https://api.rawg.io/api/games?key={rawg_key}&search={modified_string}"
    response = requests.get(url)
    data = response.json()
    #print(data["results"][0]["id"])
    return data["results"][0]["id"]

def game_data(id):
    url = f"https://api.rawg.io/api/games/{id}?key={rawg_key}"
    print(url)
    response = requests.get(url)
    data = response.json()
    print(data)

my_id_test = game_id_grabber()
game_data(my_id_test)