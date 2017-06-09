$(document).ready(function () {
    var notification_count = $("#notification_count");
    $.get(notification_count.attr("data-ajax-target"),
        function (data) {
            console.log("count:" + data.count);
            $("#notification_count").html(data.count);
        }, "json");
});
