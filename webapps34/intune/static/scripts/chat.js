$(document).ready(function() {
    // Top level module definitions
    // One chat_box per composition
    var chat_box = $("#chat_box");
    var room_id = chat_box.attr("data-room-id");
    var username = chat_box.attr("data-username");
    var user_id = chat_box.attr("data-user-id");
    var socket = new WebSocket("ws://" + window.location.host + "/chat/" + room_id + "/");

    var unread_chat = $("#unread_chats");

    // Socket message receiver
    socket.onmessage = function (msg_json) {
        var msg_data = JSON.parse(msg_json.data);

        var msg_div = $(
            "<div class='message'><strong>" +  msg_data["user"] + ": </strong>" + msg_data["msg"] +
            "<span class='pull-right text-muted small'> Just now</span></div>"
        );

        var msg_list = $("#message_list");
        msg_list.append(msg_div);

        // auto scroll to bottom of chat
        msg_list.scrollTop(msg_list[0].scrollHeight);

        // If chat is hidden, message can't be read, so update unread counter
        if ($("#chat_box").hasClass("hidden")) {
            var current_unread = unread_chat.html();
            if (current_unread) {
                current_unread = parseInt(current_unread);
            }
            unread_chat.html(current_unread + 1);
        }
    };

    // Socket open handler
    socket.onopen = function() {
        // Message sender
        $("#chat-msg").submit(function() {
            var msg_send = $("#msg-text");
            var text = msg_send.val();
            var msg = {
                "room": room_id,
                "msg": text,
                "user": user_id
            };
            socket.send(JSON.stringify(msg));
            event.preventDefault();
            msg_send.val("");
        });
    };

    function _adapt_chat_height() {
        "use strict";
        var window_height = $(window).height();
        // Hardcoded
        var max_height = window_height - 450;
        if (max_height < 0) {
            max_height = 0;
        }
        console.log("Max Height: " + max_height);
        $("#message_list").css("max-height", max_height + "px");
    }

    // Register event triggers
    $("#open-chat-button").click(function() {
        if (chat_box.hasClass("hidden")) {
            // Chat hidden, reveal it
            chat_box.removeClass("hidden");
            unread_chat.html("");
        } else {
            // Chat is open, hide it
            chat_box.addClass("hidden");
        }
    });

    $(window).resize(function() {
        "use strict";
       _adapt_chat_height();
    });

    /* Initialisation Code */

    // Resize height on first load
    _adapt_chat_height();
    // Hide chat
    if (!chat_box.hasClass("hidden")) {
        chat_box.addClass("hidden");
    }
});
