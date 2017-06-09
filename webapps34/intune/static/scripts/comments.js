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
        function _submit_comment() {
            var bar_count = Editor.get_bar_count();
            var current_bar = Editor.get_current_bar();

            if (current_bar < 0 || current_bar >= bar_count) {
                // Verify valid bar
                console.log("No bar selected to comment on");
            } else {
                var comment_form = $("#comment_form");

                var form_data = {
                    'composition_id': comment_form.attr("data-composition-id"),
                    'bar_id': current_bar,
                    'comment': $("#comment_text").val()
                };

                $.ajax({
                    type: comment_form.attr('method'),
                    url: comment_form.attr('action'),
                    data: form_data,
                    dataType: "json",
                    encode: true
                }).done(function (result) {
                    if (result.success) {
                        $('#comment_text').val("");
                    }

                    _retrieve_comments(current_bar);
                });
            }
            event.preventDefault();
        }

        /**
         * Retrieves comments that correspond to the current_bar index
         * @param current_bar: Bar index
         * @private
         */
        function _retrieve_comments(current_bar) {
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
            for (var i = 0; i < comments.comments.length; i++) {
                var comment_element = document.createElement("div");
                comment_element.setAttribute("class", "comment-element");
                comment_element.id = "comment-element-" + i;
                document.getElementById("comments").appendChild(comment_element);

                var name_col = document.createElement("div");
                name_col.setAttribute("class", "comment col-sm-8");
                name_col.id = "text" + i;
                document.getElementById("comment-element-" + i).appendChild(name_col);
                document.getElementById("text" + i).innerHTML = "<p><b>" + comments.comments[i].commenter + "</b>: " + comments.comments[i].comment + "</p>";

                // var comment_col = document.createElement("div");
                // comment_col.setAttribute("class", "comment col-sm-6");
                // comment_col.id = "comment";
                // document.getElementById("comment-element").appendChild(comment_col);
                // document.getElementById("comment").innerHTML = "<p>" + comments.comments[i].comment + "</p>";

                var time_col = document.createElement("div");
                time_col.setAttribute("class", "comment col-sm-4");
                time_col.id = "time" + i;
                document.getElementById("comment-element-" + i).appendChild(time_col);
                var time = new Date(comments.comments[i].time);
                var hours = ('0' + time.getHours()).slice(-2);
                var mins = ('0' + time.getMinutes()).slice(-2);
                document.getElementById("time" + i).innerHTML = "<p>" + hours + ":" + mins + " " + time.toDateString() + "</p>";
            }
        }

        return {
            submit_comment: _submit_comment,
            retrieve_comments: _retrieve_comments
        }
    })();

    var comment_form = $("#comment_form");
    comment_form.hide();

    comment_form.submit(BarComment.submit_comment);
});
