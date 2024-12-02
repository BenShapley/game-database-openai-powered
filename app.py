from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', question="Type question here!", chatbot_response="", background_image="")

@app.route('/', methods=['POST'])
def index_post():
	user_question = request.form['req_question']
	chatbot_response = main.ask_question(user_question)
	get_image = main.game_screenshots(user_question)
	return render_template('index.html', question=user_question, chatbot_response=chatbot_response, background_image=get_image)