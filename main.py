import json
import requests

with open("keys/rawg_keys.json", "r") as rawg_files:
    rawg_keys = json.load(rawg_files)

rawg_key = rawg_keys["client_key"]

test_input = input("Enter a game name:")
modified_string = test_input.replace(" ", "%20")

# Gets a games ID based on a user search
# TODO = add user search as an input / replaced modified_string
def game_id_grabber():
    url = f"https://api.rawg.io/api/games?key={rawg_key}&search={modified_string}"
    response = requests.get(url)
    data = response.json()
    return data["results"][0]["id"]

# Returns game data for use
def game_data(id):
    url = f"https://api.rawg.io/api/games/{id}?key={rawg_key}"
    print(url)
    response = requests.get(url)
    data = response.json()
    return data

# Returns game description
def game_description(id):
    data = game_data(id)
    description = data["description_raw"]
    return description

# Returns ratings condensed
def game_ratings(id):
    data = game_data(id)
    ratings = data["ratings"]
    ratings_data = [{"title": rating["title"], "percent": rating["percent"]} for rating in ratings]
    for i in ratings_data:
        print(i)

# Returns game screenshots
def game_screenshots(id):
    url = f"https://api.rawg.io/api/games/{id}/screenshots?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    screenshots = data["results"]
    for sc in screenshots:
        print(sc["image"])

# Returns reddit URL
def game_reddit_url(id):
    data = game_data(id)
    reddit_url = data["reddit_url"]
    if reddit_url:
        return reddit_url
    else:
        return "No reddit"

# Returns game platforms
def game_platforms(id):
    data = game_data(id)
    game_platforms = data["parent_platforms"]
    platforms = [i["platform"]["name"] for i in game_platforms]
    for i in platforms:
        print(i)

my_id_test = game_id_grabber()
game_description(my_id_test)