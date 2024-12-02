from flask import Flask, render_template, request
from main import ask_question

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', question="Type question here!", chatbot_response="")

@app.route('/', methods=['POST'])
def index_post():
	user_question = request.form['req_question']
	chatbot_response = ask_question(user_question)
	return render_template('index.html', question=user_question, chatbot_response=chatbot_response)