$( document ).ready(function() {
    console.log( "ready!" );
    var room_id = roomId = $("div.roomdiv").attr("data-room-id");
    var socket = new WebSocket("ws://" + window.location.host + "/chat-" + room_id + "/");
    socket.connect
    socket.onmessage = function (e) {
        console.log("Got message")
        var username = $("div.roomdiv").attr("data-username");
        var msg_div = $(
            "<div class='messages'>" + username + ": " + e.data + "</div>"
        );
        $("#chats").append(msg_div);
    }

    socket.onopen = function () {
        console.log("Socket Connected")

        $("#send-msg").click (function() {
            var text = $("div.roomdiv").find("input").val()
            var room_id = roomId = $("div.roomdiv").attr("data-room-id");
            msg = {
                "room": room_id,
                "msg": text,
            }
            console.log("text = ", msg)
            socket.send(JSON.stringify(msg));
        });
    }
});