from flask import Flask, render_template, request, jsonify
import openai
from ChatBot1 import chatbot

import os  # Importado para usar variables de entorno

app = Flask(__name__)

# Usa variables de entorno para tus claves y credenciales
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    response = chatbot(msg)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

