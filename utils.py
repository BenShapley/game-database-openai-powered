import json
import requests
import random

with open("keys/rawg_keys.json", "r") as rawg_files:
    rawg_keys = json.load(rawg_files)
rawg_key = rawg_keys["client_key"]
base_url = rawg_keys["base_url"]

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
    return ratings_data

# Returns game screenshots
def game_screenshots(user_input):
    id = game_id_grabber(user_input)
    url = base_url+f"/{id}/screenshots?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    screenshots = data["results"]
    i = random.randrange(0,len(screenshots))
    if screenshots:
        return screenshots[i]["image"]
    else:
        return ""

# Returns reddit URL
def game_reddit_url(id):
    data = game_data(id)
    reddit_url = data["reddit_url"]
    posts_url = base_url+f"/{id}/reddit?key={rawg_key}"
    response = requests.get(posts_url)
    recent_reddit_posts = response.json()
    if reddit_url:
        return reddit_url, recent_reddit_posts
    else:
        return "No reddit", ""

# Returns game platforms
def game_platforms(id):
    data = game_data(id)
    game_platforms = data["parent_platforms"]
    platforms = [i["platform"]["name"] for i in game_platforms]
    return platforms

# Returns game stores
def game_stores(id):
    url = base_url+f"/{id}/stores?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Returns game genres
def game_genres(id):
    data = game_data(id)
    desired_data = data["genres"]
    genres = [i["name"] for i in desired_data]
    max_count = 12
    for i in genres:
        print(i)
    if len(genres) > max_count:
        return genres[:max_count]
    return genres

# Returns game achievements and amount
def game_achievements(id):
    url = base_url+f"/{id}/achievements?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    return data["results"], data["count"]

# Returns the main game developer
def game_developer(user_input):
    desired_id = game_id_grabber(user_input)
    desired_data = game_data(desired_id)
    developer = desired_data["developers"]
    if developer:
        main_dev = desired_data["developers"][0]["name"]
        return main_dev
    else:
        return ""

# Returns most popular game of a year
def most_popular_game_by_year(date):
    url = base_url+f"?key={rawg_key}&dates={date}&ordering=-added"
    response = requests.get(url)
    data = response.json()
    popular_game = data["results"][0]
    return popular_game