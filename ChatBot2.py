from pymongo import MongoClient
import openai
import datetime

# Conexión a la base de datos MongoDB
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://kibo:kibo@cluster0.ja6e1x6.mongodb.net/?retryWrites=true&w=majority")
    db = client["FOODCHAT"]
    recetas_collection = db["recetas"]
    conversaciones_collection = db["conversaciones"]
    return recetas_collection, conversaciones_collection

# Configura tu clave de API de OpenAI
openai.api_key = "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"

# Funciones de interacción con el chatbot
def chatbot(msg):
    recetas_collection, conversaciones_collection = connect_to_mongodb()

    if "recetas" in msg:
        return mostrar_recetas_disponibles(recetas_collection)
    else:
        response = generar_respuesta(msg, recetas_collection, conversaciones_collection)
        
        # Guardar la conversación y respuesta en la base de datos
        guardar_conversacion(msg, response, conversaciones_collection)
        
        return response


def guardar_conversacion(input_text, respuesta, conversaciones_collection):
    timestamp = datetime.datetime.now()

    conversacion = {
        "fecha": timestamp,
        "entrada_usuario": input_text,
        "respuesta_chatbot": respuesta
    }

    conversaciones_collection.insert_one(conversacion)

def mostrar_recetas_disponibles(recetas_collection):
    recetas = recetas_collection.find()
    recetas_lista = ["Recetas disponibles:"]
    for receta in recetas:
        recetas_lista.append(receta["titulo"])
    return "\n".join(recetas_lista)

        
def generar_respuesta(input_text, recetas_collection, conversaciones_collection):
    respuesta_guardada = buscar_respuesta_guardada(input_text, conversaciones_collection)
    
    if respuesta_guardada:
        return respuesta_guardada
    recetas = recetas_collection.find()
    respuesta = ""

    for receta in recetas:
        if receta["titulo"].lower() in input_text:
            titulo = receta["titulo"]
            ingredientes = "\n".join(receta.get("ingredientes", []))
            pasos = "\n".join(receta.get("pasos", []))
            tiempo = receta.get("tiempo_preparacion", 0)
            porciones = receta.get("porciones", 1)
            tipo = receta.get('tipo_cocina', 1)

            tiempo_minutos = f"{tiempo} minutos"
            tiempo_horizontal = "".join(tiempo_minutos)

            porciones_texto = f"{porciones} porciones"
            porciones_horizontal = "".join(porciones_texto)
            tipos = f"Cocina {tipo}"
            tipo_horizontal = "".join(tipos)

            respuesta = f"Aquí tienes la receta de '{titulo}':\n\nIngredientes:\n{ingredientes}\n\nPasos:\n{pasos}:\n\nTiempo de Preparación:\n{tiempo_horizontal}:\n\nPorciones:\n{porciones_horizontal}:\n\nTipo de cocina:\n{tipo_horizontal}"
            break

    if not respuesta:
        respuesta = get_openai_response(input_text)

    return respuesta

def buscar_respuesta_guardada(input_text, conversaciones_collection):
    # Buscar en la base de datos si hay una respuesta guardada para el input
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
    chatbot()