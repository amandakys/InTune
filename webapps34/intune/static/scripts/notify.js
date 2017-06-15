$(document).ready(function () {
    var notification_counter = $("#notification_counter");
    var notification_menu = $("#notification-menu")
    var socket = new WebSocket("ws://" + window.location.host + "/notifications/");
    var notification_count = -1;
    var received = false;

    socket.onmessage = function (e) {
        var data = JSON.parse(e.data);

        function update_notification_count(count) {
            notification_count = count;
            if (notification_count != 0) {
                notification_counter.html(notification_count);
            }
        }

        function prepend_notification(notification) {
            if (received === false) {
                received = true;
                notification_menu.html("");
            }
            notification_menu.prepend(
                $('<li>').append($('<a>', {
                    "href": notification["link"],
                    "html": notification["msg"] + " at " + notification["time"]
                }))
            );
        }

        if (data["action"] == "unread_count") {
            update_notification_count(data["unread"]);
            for (var i = data["notification_list"].length - 1; i >= 0; i--) {
                prepend_notification(data["notification_list"][i]);
            }
        } else {
            update_notification_count(notification_count + 1);
            prepend_notification(data);
        }
    };
});
