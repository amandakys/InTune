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

        function prepend_notification(message, time, link) {
            var notif_msg = "<div class='notification col-sm-8'><p>" + message + "</p></div>";
            var notif_time = "<div class='notification col-sm-4'><p> Just now </p></div>";
            var notif_li =
                "<li><div class='composition-element notification-element'>" + notif_msg + notif_time + "</div></li>";
            notification_menu.prepend(notif_li);
        }

        if (data["action"] == "unread_count") {
            update_notification_count(data["unread"]);
            console.log(data['notification_list'])
            for (var i=0; i < data["notification_list"].length; i++) {
                console.log("HEllo");
                var notification = data["notification_list"][i];
                prepend_notification(notification["msg"], notification["time"], notification["link"]);
            }
        } else {
            update_notification_count(notification_count + 1);
            prepend_notification(data["msg"], null, null);
        }
    };
});
