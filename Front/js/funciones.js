function mostrarDescripcion(id) {
    let descripcion = document.getElementById(id);
    if (descripcion.style.display === "block") {
        descripcion.style.display = "none";
    } else {
        let todasLasDescripciones = document.querySelectorAll('.descripcion');
        todasLasDescripciones.forEach((desc) => desc.style.display = 'none');
        descripcion.style.display = "block";
    }
}

function openChat() {
    $("#chatbox").toggle();
}

function sendMessage() {
    const userMessage = $("#user_input").val();
    $("#messages").append("<p>Tú: " + userMessage + "</p>");
    
    $.post("/ask", {user_message: userMessage}, function(data) {
        $("#messages").append("<p>Bot: " + data.response + "</p>");
    });

    $("#user_input").val('');
}
