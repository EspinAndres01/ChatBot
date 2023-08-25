from pymongo import MongoClient
import openai
import datetime
from flask import Flask, render_template, request
app = Flask(__name__)

def connect_to_mongodb():
    client = MongoClient("mongodb+srv://kibo:kibo@cluster0.ja6e1x6.mongodb.net/?retryWrites=true&w=majority")
    db = client["FOODCHAT"]
    return db["recetas"], db["conversaciones"]

recetas_collection, conversaciones_collection = connect_to_mongodb()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["userInput"]
        response = generar_respuesta(user_input)
        guardar_conversacion(user_input, response)
        return render_template("chat.html", response=response)
    return render_template("chat.html")

openai.api_key = "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"  # Store it securely

def guardar_conversacion(input_text, respuesta):
    timestamp = datetime.datetime.now()
    conversacion = {
        "fecha": timestamp,
        "entrada_usuario": input_text,
        "respuesta_chatbot": respuesta
    }
    conversaciones_collection.insert_one(conversacion)

def generar_respuesta(input_text):
    respuesta_guardada = buscar_respuesta_guardada(input_text)
    if respuesta_guardada:
        return respuesta_guardada
    
    respuesta = ""
    for receta in recetas_collection.find():
        if receta["titulo"].lower() in input_text:
            respuesta = ...  # Same as your code
            break

    if not respuesta:
        respuesta = get_openai_response(input_text)
    
    return respuesta

def buscar_respuesta_guardada(input_text):
    conversacion = conversaciones_collection.find_one({"entrada_usuario": input_text})
    if conversacion:
        return conversacion["respuesta_chatbot"]
    return None

def get_openai_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=300,
        temperature=0.2
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)