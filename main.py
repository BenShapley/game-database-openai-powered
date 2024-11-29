import json
import requests
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key = os.getenv("AZURE_KEY"),
    azure_endpoint = os.getenv("AZURE_ENDPOINT"),
    api_version = "2023-10-01-preview"
)

messages = [
	{"role": "system", "content": "PERSONALITY"},
]

with open("keys/rawg_keys.json", "r") as rawg_files:
    rawg_keys = json.load(rawg_files)
rawg_key = rawg_keys["client_key"]

base_url = "https://api.rawg.io/api/games"

# Gets a games ID based on a user search
def game_id_grabber(user_search):
    modified_string = user_search.replace(" ", "%20")
    url = base_url+f"?key={rawg_key}&search={modified_string}"
    print(url)
    response = requests.get(url)
    data = response.json()
    return data["results"][0]["id"]

# Returns game data for use
def game_data(id):
    url = base_url+f"/{id}?key={rawg_key}"
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
    return ratings_data

# Returns game screenshots
def game_screenshots(id):
    url = base_url+f"/{id}/screenshots?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    screenshots = data["results"]
    for sc in screenshots:
        print(sc["image"])
    return screenshots

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
    return platforms

def game_stores(id):
    url = base_url+f"/{id}/stores?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    print(data)

test_input = input("Enter a game name:")
my_id_test = game_id_grabber(test_input)
game_stores(my_id_test)