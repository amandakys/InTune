$(document).ready(function () {
    var notification_counter = $("#notification_counter");
    var socket = new WebSocket("ws://" + window.location.host + "/notifications/");
    var notification_count = -1;

    socket.onmessage = function (e) {
        var data = JSON.parse(e.data);

        function update_notification_count(count) {
            notification_count = count;
            if (notification_count != 0) {
                notification_counter.html(notification_count);
            }
        }

        if (data["action"] == "unread_count") {
            update_notification_count(data["unread"]);
        } else {
            update_notification_count(notification_count + 1);

            // live updates on notifications page
            var notif_msg = "<div class='notification col-sm-8'><p>" + data["msg"] + "</p></div>";
            var notif_time = "<div class='notification col-sm-4'><p> Just now </p></div>";
            var notif_li =
                "<li><div class='composition-element notification-element'>" + notif_msg + notif_time + "</div></li>";
            var notif_list = $("#notif-list");
            notif_list.prepend(notif_li);
        }
    };
});
