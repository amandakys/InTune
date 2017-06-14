$(document).ready(function () {
    var notification_count = $("#notification_count");
    var user_id = notification_count.attr("data-user-id");
    var socket = new WebSocket("ws://" + window.location.host + "/notif/" + user_id + "/");

    socket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        console.log("recevied notif ", data);

        // update notif count
        var current_unread = notification_count.html();
        if (current_unread) {
                current_unread = parseInt(current_unread);
            }
        notification_count.html(current_unread + 1);

        // live updates on notifications page
        var notif_msg = "<div class='notification col-sm-8'><p>" + data["msg"] + "</p></div>";
        var notif_time = "<div class='notification col-sm-4'><p> Just now </p></div>";
        var notif_li =
            "<li><div class='composition-element notification-element'>" + notif_msg + notif_time + "</div></li>";
        var notif_list = $("#notif-list");
        notif_list.prepend(notif_li);
    };

    socket.onopen = function() {
        console.log("connected!!", socket);
    }
});
