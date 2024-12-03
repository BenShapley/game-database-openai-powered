from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', question="Search...", background_image="static/default_background.png")

@app.route('/', methods=['POST'])
def index_post():
	user_question = request.form['req_question']
	chatbot_response,game_name = main.ask_question(user_question)
	get_image = main.game_screenshots(game_name)
	return render_template('search.html', question=user_question, chatbot_response=chatbot_response, background_image=get_image, 
						game=game_name, show_absolute_background=True) 