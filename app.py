from flask import Flask, render_template, request, jsonify
from ChatBot1 import chatbot

app = Flask(__name__)

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_message']
    response = chatbot(user_message)
    return jsonify({'response': response})