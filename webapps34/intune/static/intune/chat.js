$( document ).ready(function() {
    console.log( "ready!" );
    var room_id = roomId = $("div.roomdiv").attr("data-room-id");
    var username = $("div.roomdiv").attr("data-username");
    var user_id = $("div.roomdiv").attr("data-user-id");

    var socket = new WebSocket("ws://" + window.location.host + "/chat-" + room_id + "/");


    socket.connect
    socket.onmessage = function (e) {
        console.log("Got message")
        var data = JSON.parse(e.data)
        var msg_div = $(
            "<div class='messages'><span class='username'>" +  data.user + ": </span><span class='msg'>" + data.msg +  "</span><span class='time'> Just now</span></div>"
        );
        $("#chats").append(msg_div);
    }

    socket.onopen = function () {
        console.log("Socket Connected")

        $("#chat-box").submit (function() {
            var text = $("div.roomdiv").find("input").val()
            var room_id = roomId = $("div.roomdiv").attr("data-room-id");
            msg = {
                "room": room_id,
                "msg": text,
                "user": user_id
            }
            console.log("text = ", msg)
            socket.send(JSON.stringify(msg));
            event.preventDefault()
        });
    }
});