$( document ).ready(function() {
    var room_id = roomId = $("div.roomdiv").attr("data-room-id");
    var username = $("div.roomdiv").attr("data-username");
    var user_id = $("div.roomdiv").attr("data-user-id");
    var socket = new WebSocket("ws://" + window.location.host + "/chat/" + room_id + "/");

    socket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        var msg_div = $(
            "<div class='messages'><strong>" +  data.user + ": </strong>" + data.msg +
            "<span class='pull-right text-muted small'> Just now</span></div>"
        );
        $("#chats").append(msg_div);

        // auto scroll to bottom of chat
        $("#chats").scrollTop($("#chats")[0].scrollHeight);
    };

    socket.onopen = function () {
        $("#chat-box").submit (function() {
            var text = $("div.roomdiv").find("input").val();
            var room_id = roomId = $("div.roomdiv").attr("data-room-id");
            msg = {
                "room": room_id,
                "msg": text,
                "user": user_id,
            };
            socket.send(JSON.stringify(msg));
            event.preventDefault();
            $("#chat-msg").val("");
        });
    }
});
