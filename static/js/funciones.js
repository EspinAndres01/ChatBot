function mostrarDescripcion(id) {
    let descripcion = $(`#${id}`);
    if (descripcion.css("display") === "block") {
        descripcion.css("display", "none");
    } else {
        $('.descripcion').css("display", 'none');
        descripcion.css("display", "block");
    }
}

function openChat() {
    $("#chatbox").toggle();
}

function sendMessage() {
    const userMessage = $("#userInput").val();
    $("#messages").append("<p>Tú: " + userMessage + "</p>");
    
    $.post("/", {userInput: userMessage}, function(data) {
        $("#messages").append("<p>Bot: " + data.response + "</p>");
    }).fail(function() {
        $("#messages").append("<p>Bot: Lo siento, no pude procesar tu mensaje.</p>");
    });

    $("#userInput").val('');
}

