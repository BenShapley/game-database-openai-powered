"""
Flask App that hosts and posts to the website
Author: Ben Shapley
"""

from flask import Flask, render_template, request
import main
import utils

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', question="Search...", background_image="static/default_background.png", searching=False)

@app.route('/', methods=['POST'])
def index_post():
	user_question = request.form['req_question']
	chatbot_response,game_name = main.ask_question(user_question)
	get_image = utils.game_screenshots(game_name)
	dev = utils.game_developer(game_name)
	return render_template('search.html', question=user_question, chatbot_response=chatbot_response, background_image=get_image, 
						game=game_name, show_absolute_background=True, developer=dev, searching=False) 

@app.route('/help')
def index_help():
	return render_template('help.html', question="Give it a go...", background_image="static/default_background.png") 