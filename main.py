import json
import requests
from openai import AzureOpenAI
import os
import random

client = AzureOpenAI(
    api_key = os.getenv("AZURE_KEY"),
    azure_endpoint = os.getenv("AZURE_ENDPOINT"),
    api_version = "2023-10-01-preview"
)

messages = [
	{"role": "system", "content": """If the the user asks you what a game is about that you dont think exists,
  please check the 'get_game_description' function to find it. If the user asks where you can buy a game
  that you dont think exists, please check the 'get_game_stores' function to find it. If the user
  asks you if a game you dont think exists has a Subreddit, please check the 'get_game_reddit' function
  to find it. Can you after your reponse put a verticle bar ('|') and then name the game we are talking about with 
  title capitalisation."""},
]

with open("keys/rawg_keys.json", "r") as rawg_files:
    rawg_keys = json.load(rawg_files)
rawg_key = rawg_keys["client_key"]
base_url = rawg_keys["base_url"]

# Gets a games ID based on a user search
def game_id_grabber(user_search):
    print(user_search)
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
def game_screenshots(user_input):
    id = game_id_grabber(user_input)
    url = base_url+f"/{id}/screenshots?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    #print(data)
    screenshots = data["results"]
    i = random.randrange(0,len(screenshots))
    if screenshots:
        # for sc in screenshots:
        #     print(sc["image"])
        return screenshots[i]["image"]
    else:
        return ""

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

# Returns game stores
def game_stores(id):
    url = base_url+f"/{id}/stores?key={rawg_key}"
    response = requests.get(url)
    data = response.json()
    #print(data)
    return data

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

functions = [
	{
		"type": "function",
		"function": {
			"name": "get_game_description",
			"description": """Only returns what a desired game is about and provides a description.
            An example would be someone asking 'What is the game [name] about?'""",
			"parameters": {
				"type": "object",
				"properties": {
					"user_input": {
						"type": "string",
						"description": "The video game title you are using to search"
					}
				},
				"required": ["user_input"]
            }
		},
        "type": "function",
        "function": {
            "name": "get_game_stores",
			"description": """Returns where the user can buy/get a desired game.
            An example would be someone asking 'Where can I get/buy the game [name] from?'""",
			"parameters": {
				"type": "object",
				"properties": {
					"user_input": {
						"type": "string",
						"description": "The video game title you are using to search"
					}
				},
				"required": ["user_input"]
            }
        },
        "type": "function",
        "function": {
            "name": "get_game_reddit",
			"description": """Only returns a games Reddit page.
            An example would be someone asking 'Does the game [name] have a reddit or social media'""",
			"parameters": {
				"type": "object",
				"properties": {
					"user_input": {
						"type": "string",
						"description": "The video game title you are using to search"
					}
				},
				"required": ["user_input"]
            }
        },
        "type": "function",
        "function": {
            "name": "get_game_reviews",
			"description": """Returns reviews and what people think about a desired game.
            An example would be someone asking 'What do people think/how good is the game [name]'""",
			"parameters": {
				"type": "object",
				"properties": {
					"user_input": {
						"type": "string",
						"description": "The video game title you are using to search"
					}
				},
				"required": ["user_input"]
            }
        },
        "type": "function",
        "function": {
            "name": "get_game_platforms",
			"description": """Returns the platforms that you can play the desired game on.
            An example would be someone asking 'What can I play [name] on?'""",
			"parameters": {
				"type": "object",
				"properties": {
					"user_input": {
						"type": "string",
						"description": "The video game title you are using to search"
					}
				},
				"required": ["user_input"]
            }
        },
        "function": {
            "name": "compare_games",
			"description": """Compares two games together to see how each one were recieved by the public
            An example would be someone asking 'What game is better, [name] or [name]?'""",
			"parameters": {
				"type": "object",
				"properties": {
					"user_input_x": {
						"type": "string",
						"description": "The first video game title you are using to search"
					},
                    "user_input_y": {
						"type": "string",
						"description": "The second video game title you are using to search"
					}
				},
				"required": ["user_input_x", "user_input_y"]
            }
        }
	}
]

# OpenAI function to return a game description
def get_game_description(user_input):
    print("FETCHING DESCRIPTION")
    desired_id = game_id_grabber(user_input)
    desired_data = game_description(desired_id)
    return f"""The {user_input} game is described as {desired_data}.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> paragraphs 
    and <br> breaks where necessary. Please use HTML styling to spice it up!!! Maybe use background colors with border styling or cool
    text styling for example. Try to match the styling with the game theme though. Keep in mind, the background is BLACK and i want the
    text always to be a white or LIGHT color. So keep the background dark as well."""

# OpenAI function to return where a game can be bought
def get_game_stores(user_input):
    print("FETCHING STORES")
    desired_id = game_id_grabber(user_input)
    desired_data = game_stores(desired_id)
    return f"""You can buy the game {user_input} in these stores: {desired_data}.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> paragraphs 
    and <li> lists where necessary so it displays. Please present these nicely and make it interesting by using some styling to spice 
    it up!! Just keep in mind, the background is black so make sure it is visible."""

# OpenAI function to return a game reddit if it exists
def get_game_reddit(user_input):
    print("FETCHING REDDIT")
    desired_id = game_id_grabber(user_input)
    desired_data = game_reddit_url(desired_id)
    return f"""If the game {user_input} has a reddit, it may be here{desired_data}.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> paragraphs 
    and <br> breaks where necessary. Please present these nicely and make it interesting by using some styling to spice 
    it up!! Just keep in mind, the background is black so make sure it is visible."""

# OpenAI function to return reviews about a game
def get_game_reviews(user_input):
    print("FETCHING REVIEWS")
    desired_id = game_id_grabber(user_input)
    desired_data = game_ratings(desired_id)
    return f"""Format the ratings ({desired_data}) of the game {user_input} by presenting it professionally.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> and <li>
    where necessary. Please use HTML styling to spice it up!!! For eg, use colours! Just keep in mind, the background is black so
    make sure its visible."""

def get_game_platforms(user_input):
    print("FETCHING PLATFORMS")
    desired_id = game_id_grabber(user_input)
    desired_data = game_platforms(desired_id)
    return f"""Format the ratings ({desired_data}) of the game {user_input} by presenting it professionally.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> and <li>
    where necessary. Please use HTML styling to spice it up!!! For eg, use colours! Just keep in mind, the background is black so
    make sure its visible."""

def compare_games(user_input_x, user_input_y):
    desired_id_x = game_id_grabber(user_input_x)
    desired_id_y = game_id_grabber(user_input_y)
    desired_data_x = game_ratings(desired_id_x)
    desired_data_y = game_ratings(desired_id_y)
    return f"""Format the ratings of ({desired_data_x}) of the game {user_input_x} by presenting it professionally. Then
    contrast these ratings with {desired_data_y} of the game {user_input_y} to make a comprehensive comparision.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> and <li>
    where necessary. Please use HTML styling to spice it up!!! For eg, use colours! Just keep in mind, the background is black so
    make sure its visible."""

# OpenAI question input and answer
def ask_question(question):
    messages.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
		model = "GPT-4",
		messages = messages,
		tools = functions,
		tool_choice = "auto"
	)

    response_message = response.choices[0].message
    gpt_tools = response.choices[0].message.tool_calls

    if gpt_tools:
        available_functions = {
			"get_game_description": get_game_description,
            "get_game_stores" : get_game_stores,
            "get_game_reddit" : get_game_reddit,
            "get_game_reviews": get_game_reviews,
            "get_game_platforms": get_game_platforms,
            "compare_games": compare_games
		}

        messages.append(response_message)
        for gpt_tool in gpt_tools:
            function_name = gpt_tool.function.name
            function_to_call = available_functions[function_name]
            function_parameters = json.loads(gpt_tool.function.arguments)
            if function_name == "compare_games":
                function_response = function_to_call(function_parameters.get('user_input_x'), function_parameters.get('user_input_y'))
            else:
                function_response = function_to_call(function_parameters.get('user_input'))
            messages.append(
				{
					"tool_call_id": gpt_tool.id,
					"role": "tool",
					"name": function_name,
					"content": function_response
				}
			)
            second_response = client.chat.completions.create(
				model = "GPT-4",
				messages=messages
			)
            print("SUCCESS")
            #print(response)
            
            #print (second_response.choices[0].message.content)
            split_response = second_response.choices[0].message.content.split("|")
            main_response = split_response[0]
            game_name = split_response[1]
            return main_response, game_name

    else:
        print("DEFAULTED")
        return response.choices[0].message.content, ""

#test_input = input("Enter a game name:")
#game_screenshots(test_input)
#print(get_game_description(test_input))
#ask_question(test_input)