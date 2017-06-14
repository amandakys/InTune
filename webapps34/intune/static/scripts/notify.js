$(document).ready(function () {
    var notification_count = $("#notification_count");
    var user_id = notification_count.attr("data-user-id");
    var socket = new WebSocket("ws://" + window.location.host + "/notif/" + user_id + "/");

    socket.onmessage = function (e) {
        var current_unread = notification_count.html();
        if (current_unread) {
                current_unread = parseInt(current_unread);
            }
        notification_count.html(current_unread + 1);
    };
});
