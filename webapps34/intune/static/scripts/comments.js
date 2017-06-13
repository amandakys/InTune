/**
 * JS Module handling comment retrieval and updates
 * Requires:
 * 1. Editor JS Module
 *
 * Note:
 * This module does not export any APIs
 */
$(document).ready(function () {
    window.BarComment = (function () {
        "use strict";

        var comment_div = $("#comments");
        var room_id = comment_div.attr("data-room-id");
        var username = comment_div.attr("data-username");
        var user_id = comment_div.attr("data-user-id");
        var bar_id = Editor.get_current_bar();

        // connect to socket at chat-<room_id>-<bar-id>
        var socket = new WebSocket("ws://" + window.location.host + "/comment/" + room_id + "/");

        // refresh comments page onmessage
        socket.onmessage = function (e) {
            var data = JSON.parse(e.data);
            console.log("received comment ", data);

            // only show comment if its for current bar
            if (data.bar == bar_id) {
                var comment = {
                    "commenter": data["user"],
                    "time": new Date().toLocaleString(),
                    "comment": data["msg"]
                };

                // update comment count
                $("#total-comments").text(parseInt($("#total-comments").text()) + 1)

                display_new_comment(comment);
            }
        };

        socket.onopen = function () {
            var comment_form = $("#comment_form");

            comment_form.submit (function() {
                bar_id = Editor.get_current_bar();
                var text = $("#comment_text").val();
                var msg = {
                    "room": room_id,
                    "msg": text,
                    "user": user_id,
                    "bar": bar_id,
                };
                socket.send(JSON.stringify(msg));
                event.preventDefault();
                $("#comment_text").val("");
                console.log("sending comment ", socket, msg);
            });
        };

        /**
         * Retrieves comments that correspond to the current_bar index
         * @param current_bar: Bar index
         * @private
         */
        function _retrieve_comments(current_bar) {
            console.log("retrieveing comments...");
            var comment_form = $("#comment_form");

            var comments = $.getJSON($("#comments").attr("data-ajax-target"),
                {
                    composition: comment_form.attr("data-composition-id"),
                    bar: current_bar
                }
            ).done(_display_comments);

            comment_form.show();
        }

        function _display_comments(comments) {
            $('#comments').html("");
            $("#total-comments").text(comments.comments.length);
            for (var i = 0; i < comments.comments.length; i++) {
                display_new_comment(comments.comments[i])
            }
        }

        function display_new_comment(comment) {
            var comment_element = document.createElement("div");
            comment_element.setAttribute("class", "comment-element");
            document.getElementById("comments").prepend(comment_element);

            var name_col = document.createElement("div");
            name_col.setAttribute("class", "comment col-sm-8");
            comment_element.appendChild(name_col);
            name_col.innerHTML = "<p><b>" + comment.commenter + "</b>: " + comment.comment + "</p>";

            var time_col = document.createElement("div");
            time_col.setAttribute("class", "comment col-sm-4");
            comment_element.appendChild(time_col);
            var time = new Date(comment.time);
            var hours = ('0' + time.getHours()).slice(-2);
            var mins = ('0' + time.getMinutes()).slice(-2);
            time_col.innerHTML = "<p>" + hours + ":" + mins + " " + time.toDateString() + "</p>";
        }

        return {
            retrieve_comments: _retrieve_comments
        }
    })();

    var comment_form = $("#comment_form");
    comment_form.hide();
});
