from pymongo import MongoClient

# Conexión a la base de datos MongoDB
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://kibo:kibo@cluster0.ja6e1x6.mongodb.net/?retryWrites=true&w=majority")
    db = client["FOODCHAT"]
    recetas_collection = db["recetas"]
    return recetas_collection

# Funciones de interacción con el chatbot
def chatbot():
    print("¡Hola! Soy el FOODCHAT de recetas. ¿En qué puedo ayudarte?")
    
    recetas_collection = connect_to_mongodb()
    
    while True:
        user_input = input("USER: ").lower()
        
        if user_input == "salir":
            print("FOODCHAT: Hasta luego. ¡Vuelve pronto!")
            break
        elif "recetas" in user_input:
            mostrar_recetas_disponibles(recetas_collection)
        else:
            response = generar_respuesta(user_input, recetas_collection)
            print("FOODCHAT:", response)

def mostrar_recetas_disponibles(recetas_collection):
    recetas = recetas_collection.find()
    print("Recetas disponibles:")
    for receta in recetas:
        print("-", receta["titulo"])

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
