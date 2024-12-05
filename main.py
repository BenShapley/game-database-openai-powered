import json
from openai import AzureOpenAI
import os
import utils

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
  to find it. If the user asks you about achievements of a game you dont think exists, please check the 'get_game_achievements'
  function to find it. If the user asks you about the genre of a game you dont think exists, please check the 
  'get_game_genres' function to find it. If the user asks you what platforms a game you dont think exists is on,
  please check the 'get_game_platforms' to find it. If the user asks you about how well a game did/reviews
  for a game you dont think exists, please use the 'get_game_reviews' function to find it. If the user
  asks you to commpare two games you dont think exist, please use the 'compare_games' function to find it.
  If the user asks you what the most popular game of a specific year was, please use the 'get_most_popular_game_by_year'
  function to find it. Please make sure you format all of the returns so that it can go directly into a HTML page.
  This means no raw text, always wrapped in something like <p> for e.g. Can you after your reponse put a verticle bar ('|') 
  and then name the game we are talking about with title capitalisation, make sure you do this."""},
]

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
        "type": "function",
        "function": {
            "name": "get_game_genres",
			"description": """Returns the genres that correspond with the desired game.
            An example would be someone asking 'What genre is [name]?' or
            'What type of game is [name]?""",
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
            "name": "get_game_achievements",
			"description": """Returns a list of achievements for the desired game.
            An example would be someone asking 'What achievements does [name] have?' or
            'How many achievements does [name] have?""",
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
            "name": "get_most_popular_game_by_year",
			"description": """Returns the most popular game of a specific year.
            An example would be someone asking 'What was the most popular game of [year]""",
			"parameters": {
				"type": "object",
				"properties": {
					"user_input": {
						"type": "string",
						"description": """The year the user is trying to search by.
                        Format this like: '[YEAR]-01-01,[YEAR]-12-31'"""
					}
				},
				"required": ["user_input"]
            }
        },
        "type": "function",
        "function": {
            "name": "compare_games",
			"description": """Compares two games together to see how each one were recieved by the public
            An example would be someone asking 'What game is better, [name] or [name]?'
            ONLY RUN THIS FUNCTION IF TWO DIFFERENT GAMES ARE REQUESTED. If one game is requested,
            the 'get_game_reviews' would be better.""",
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
    print(user_input)
    print("FETCHING DESCRIPTION")
    desired_id = utils.game_id_grabber(user_input)
    desired_data = utils.game_description(desired_id)
    return f"""The {user_input} game is described as {desired_data}.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> paragraphs 
    and <br> breaks where necessary. Please use HTML styling to spice it up!!! Maybe use background colors with border styling or cool
    text styling for example. Try to match the styling with the game theme though. Keep in mind, the background is BLACK and i want the
    text always to be a white or LIGHT color. So keep the background dark as well."""

# OpenAI function to return where a game can be bought
def get_game_stores(user_input):
    print("FETCHING STORES")
    desired_id = utils.game_id_grabber(user_input)
    desired_data = utils.game_stores(desired_id)
    return f"""You can buy the game {user_input} in these stores: {desired_data}.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> paragraphs 
    and <li> lists where necessary so it displays. Please present these nicely and make it interesting by using some styling to spice 
    it up!! Just keep in mind, the background is black so make sure it is visible."""

# OpenAI function to return a game reddit if it exists
def get_game_reddit(user_input):
    print("FETCHING REDDIT")
    desired_id = utils.game_id_grabber(user_input)
    reddit_url, recent_posts = utils.game_reddit_url(desired_id)
    return f"""If the game {user_input} has a reddit, it may be here{reddit_url}. Showcase 3 of the bests posts too {recent_posts}.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> paragraphs 
    and <br> breaks where necessary. Please present these nicely and make it interesting by using some styling to spice 
    it up!! Just keep in mind, the background is black so make sure it is visible."""

# OpenAI function to return reviews about a game
def get_game_reviews(user_input):
    print("FETCHING REVIEWS")
    desired_id = utils.game_id_grabber(user_input)
    desired_data = utils.game_ratings(desired_id)
    return f"""Format the ratings ({desired_data}) of the game {user_input} by presenting it professionally.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> and <li>
    where necessary. Please use HTML styling to spice it up!!! For eg, use colours! Format the data into graphs or circle fills to represent
    the data. Just keep in mind, the background is black so make sure its visible."""

# OpenAI function to return platforms
def get_game_platforms(user_input):
    print("FETCHING PLATFORMS")
    desired_id = utils.game_id_grabber(user_input)
    desired_data = utils.game_platforms(desired_id)
    return f"""Format the platforms ({desired_data}) of the game {user_input} by presenting it professionally.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> and <li>
    where necessary. Please use HTML styling to spice it up!!! For eg, use colours! Put the genres themselves into blocks to look cool
    Just keep in mind, the background is black so make sure its visible."""

# OpenAI function to return game genres
def get_game_genres(user_input):
    print("FETCHING GENRES")
    desired_id = utils.game_id_grabber(user_input)
    desired_data = utils.game_genres(desired_id)
    return f"""Format the gebres ({desired_data}) of the game {user_input} by presenting it professionally.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> and <li>
    where necessary. Please use HTML styling to spice it up!!! For eg, use colours! Just keep in mind, the background is black so
    make sure its visible."""

# OpenAI function to compare two different games
def compare_games(user_input_x, user_input_y):
    print(f"COMPARING {user_input_x} and {user_input_y}")
    desired_id_x = utils.game_id_grabber(user_input_x)
    desired_id_y = utils.game_id_grabber(user_input_y)
    desired_data_x = utils.game_ratings(desired_id_x)
    desired_data_y = utils.game_ratings(desired_id_y)
    return f"""Format the ratings of ({desired_data_x}) of the game {user_input_x} by presenting it professionally. Then
    contrast these ratings with {desired_data_y} of the game {user_input_y} to make a comprehensive comparision.
    I am putting this directly into a HTML document so please format this correctly. You must present the data using <p> and <li>
    where necessary. Please use HTML styling to spice it up!!! For eg, use colours! Just keep in mind, the background is black so
    make sure its visible."""

# OpenAI function to get game achievements
def get_game_achievements(user_input):
    print("FETCHING ACHIEVEMENTS")
    desired_id = utils.game_id_grabber(user_input)
    achievements, count = utils.game_achievements(desired_id)
    return f"""The game {user_input} has {count} achievements. These achievements are {achievements}. I am putting these
    achievements into a HTML document directly so please format this correctly. You must present the data using <p> and <li> when 
    necessary (EMBEDD THIS PROPERLY INTO HTML SO THAT IT SHOWS IN <p> and <li>. No raw text allowed.). I want you to showcase three 
    of the best achievements alongside embedding their  image. Just keep in mind, the background is black so make sure its visible."""

def get_most_popular_game_by_year(user_input):
    print("GETTING POPULAR GAME")
    desired_data = utils.most_popular_game_by_year(user_input)
    return f"""The most popular game within the year {user_input} was {desired_data}. I am putting this into a HTML document
    directly so please format this correctly. You must present the data using <p> and <br> when necessary (EMBEDD THIS INTO
    HTML). I want you to spice it up by using html styling!!"""

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

    print(response_message)

    if gpt_tools:
        available_functions = {
			"get_game_description": get_game_description,
            "get_game_stores" : get_game_stores,
            "get_game_reddit" : get_game_reddit,
            "get_game_reviews": get_game_reviews,
            "get_game_platforms": get_game_platforms,
            "get_game_genres": get_game_genres,
            "get_game_achievements": get_game_achievements,
            "get_most_popular_game_by_year": get_most_popular_game_by_year,
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
            split_response = second_response.choices[0].message.content.split("|")
            main_response = split_response[0]
            game_name = split_response[1]
            return main_response, game_name

    else:
        print("DEFAULTED")
        return response.choices[0].message.content, ""