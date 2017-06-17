$(document).ready(function() {
    // Top level module definitions
    // One chat_box per composition
    var chat_box = $("#chat_box");
    var room_id = chat_box.attr("data-room-id");
    var username = chat_box.attr("data-username");
    var user_id = chat_box.attr("data-user-id");
    var socket = new WebSocket("ws://" + window.location.host + "/chat/" + room_id + "/");
    var message_list = $("#message_list");

    var unread_chat = $("#unread_chats");

    function _append_message(msg_data) {
        var date_span = $('<span>', {
            "class": 'pull-right text-muted small moment-date',
            "data-date": msg_data["time"]
        });
        var msg_div = $('<div>', {
            "class": "message",
            "html": "<strong>" +  msg_data["user"] + ": </strong>" + msg_data["msg"]
        }).append(date_span);
        Moments.relative_date(date_span);

        message_list.append(msg_div);
    }

    function _append_messages(messages) {
        for (var i = 0; i < messages.length; i++)
            _append_message(messages[i]);

        // auto scroll to bottom of chat
        message_list.scrollTop(message_list[0].scrollHeight);
    }

    // Socket message receiver
    socket.onmessage = function(msg_json) {
        data = JSON.parse(msg_json.data);
        _append_messages(data["messages"]);

        // If chat is hidden, message can't be read, so update unread counter
        if (!data["initial"] && $("#chat_box").hasClass("hidden")) {
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

    function _adapt_chat_width() {
        "use strict";
        var col_2_width = $(".col-md-2.col-sm-3").width();

        var chat_box = $("#chat_box");
        chat_box.width(col_2_width);
        chat_box.css("padding-right", "15px");
    }

    function _adapt_chat_height() {
        "use strict";
        var window_height = $(window).height();
        // Hardcoded
        var max_height = window_height - 375;
        if (max_height < 0) {
            max_height = 0;
        }

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

    /**
     * Resize listener to adapt chat dimensions
     */
    $(window).resize(function() {
        "use strict";
       _adapt_chat_height();
       _adapt_chat_width();
    });

    /* Initialisation Code */

    // Resize dimensions on first load
    _adapt_chat_height();
    _adapt_chat_width();

    // Hide chat initially
    if (!chat_box.hasClass("hidden")) {
        chat_box.addClass("hidden");
    }
});
