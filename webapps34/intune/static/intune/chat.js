$( document ).ready(function() {
    console.log( "ready!" );

    var socket = new WebSocket("ws://" + window.location.host);
    socket.onmessage = function (e) {
        console.log("Got message")
        var msg_div = $(
            "<div class='messages'>" + e.data + "</div>"
        );
        $("#chats").append(msg_div);
    }

    socket.onopen = function () {
        console.log("Socket Connected")

        $("#send-msg").click (function() {
            var text = $("div.roomdiv").find("input").val()
            console.log("text = ", text)
            socket.send(text)
        });
    }
});