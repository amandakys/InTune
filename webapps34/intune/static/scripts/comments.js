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

        var comment_div = $("#comment-block");
        var comment_form = $("#comment_form");
        var room_id = comment_div.attr("data-room-id");

        // connect to socket at chat-<room_id>-<bar-id>
        var socket = new WebSocket("ws://" + window.location.host + "/comment/" + room_id + "/");


        comment_form.hide();
        // refresh comments page
        socket.onmessage = function (e) {
            var data = JSON.parse(e.data);

            // only show comment if its for current bar
            if (parseInt(data.bar) === Editor.get_current_bar()) {
                var comment = {
                    "commenter": data["user"],
                    "time": new Date(),
                    "comment": data["msg"]
                };

                // update comment count
                var total_comments = $("#total-comments");
                total_comments.text(parseInt(total_comments.text()) + 1);

                _display_new_comment(comment);
            }
        };

        socket.onopen = function () {
            comment_form.submit (function() {
                var comment_text = $("#comment_text");
                var text = comment_text.val();

                var msg = {
                    "msg": text,
                    "bar": Editor.get_current_bar()
                };

                socket.send(JSON.stringify(msg));
                event.preventDefault();
                comment_text.val("");
            });
        };

        /**
         * Retrieves comments that correspond to the current_bar index
         * @param current_bar: Bar index
         * @private
         */
        function _retrieve_comments(current_bar) {
            // Reset comment display
            comment_div.empty();
            $("#comment_form").removeClass("hide")
            $.getJSON(comment_div.attr("data-ajax-target"),
                {
                    composition: comment_form.attr("data-composition-id"),
                    bar: current_bar
                }
            ).done(_display_comments);

            comment_form.show();
        }

        /**
         *
         * @param comments_json
         * @private
         */
        function _display_comments(comments_json) {
            $("#total-comments").text(comments_json["comments"].length);
            for (var i = 0; i < comments_json["comments"].length; i++) {
                _display_new_comment(comments_json["comments"][i])
            }
        }

        /**
         *
         * @param comment_json
         * @private
         */
        function _display_new_comment(comment_json) {
            // Create new row in table
            var comment = document.createElement("p");

            // Commenter
            var commenter = document.createElement("span");
            commenter.setAttribute("class", "comment-user");
            commenter.innerHTML = comment_json["commenter"] + ": ";
            // Text
            var text = document.createElement("span");
            text.setAttribute("class", "comment-text");
            text.innerHTML = comment_json["comment"];

            comment.appendChild(commenter);
            comment.appendChild(text);

            var date = document.createElement("p");
            date.setAttribute("class", "comment-date");
            var time = new Date(comment_json.time);
            var hours = ('0' + time.getHours()).slice(-2);
            var min = ('0' + time.getMinutes()).slice(-2);
            date.innerHTML = hours + ":" + min + " " + time.toDateString();

            var comment_row = document.createElement("div");
            comment_row.setAttribute("class", "comment-element");
            comment_row.appendChild(comment);
            comment_row.appendChild(date);
            comment_div.prepend(comment_row);
        }

        return {
            retrieve_comments: _retrieve_comments
        }
    })();
});
