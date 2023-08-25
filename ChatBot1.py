from pymongo import MongoClient

# Conexión a la base de datos MongoDB
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://kibo:kibo@cluster0.ja6e1x6.mongodb.net/?retryWrites=true&w=majority")
    db = client["FOODCHAT"]
    recetas_collection = db["recetas"]
    return recetas_collection

# Función modificada de interacción con el chatbot
def chatbot(user_input):
    user_input = user_input.lower()
    
    recetas_collection = connect_to_mongodb()
    
    if "recetas" in user_input:
        return mostrar_recetas_disponibles(recetas_collection)
    else:
        response = generar_respuesta(user_input, recetas_collection)
        return response

def mostrar_recetas_disponibles(recetas_collection):
    recetas = recetas_collection.find()
    titulos = [receta["titulo"] for receta in recetas]
    return "Recetas disponibles: " + ", ".join(titulos)

def generar_respuesta(input_text, recetas_collection):
    recetas = recetas_collection.find()
    respuesta = "Lo siento, no tengo información sobre esa receta."

    for receta in recetas:
        if receta["titulo"].lower() in input_text:
            titulo = receta["titulo"]
            ingredientes = "\n".join(receta.get("ingredientes", []))
            pasos = "\n".join(receta.get("pasos", []))
            tiempo = receta.get("tiempo_preparacion", 0)
            porciones = receta.get("porciones", 1)
            tipo=receta.get('tipo_cocina',1)

            tiempo_minutos = f"{tiempo} minutos"
            tiempo_horizontal = "".join(tiempo_minutos)

            porciones_texto = f"{porciones} porciones"
            porciones_horizontal = "".join(porciones_texto)
            tipos=f"Cocina {tipo}"
            tipo_horizontal="".join(tipos)
            respuesta = f"Aquí tienes la receta de '{titulo}':\n\nIngredientes:\n{ingredientes}\n\nPasos:\n{pasos}:\n\nTiempo de Preparacion:\n{tiempo_horizontal}:\n\nPorciones:\n{porciones_horizontal}:\n\nTipo de cocina:\n{tipo_horizontal}"
            break

    return respuesta

if __name__ == "__main__":
    chatbot()
