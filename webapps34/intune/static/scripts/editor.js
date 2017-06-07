/**
 * Editor Interface APIs
 */
$(document).ready(function () {
    // Enforce module to load only when DOM is ready

    // Module "Editor"
    var Editor = (function () {
        "use strict";
        // Module specific constants
        var MAX_BARS = 5;

        // Module specific variables
        var bar_count = 0;

        // Appends a new bar to render block
        function _append_new_bar() {
            if (bar_count < MAX_BARS) {
                bar_count++;
                var canvas = document.createElement('canvas');
                canvas.id = 'bar' + bar_count;
                canvas.setAttribute("class", "bar-block");
                document.getElementById('render_block').appendChild(canvas);

                var canvas_size = {width: canvas.offsetWidth};
                Render.render_bar(canvas.id, canvas_size, "");
            } else {
                console.log("Maximum bars that can be rendered has been reached.");
            }
        }

        function _remove_bar(index) {
            if (index > bar_count) {
                // Bar does not exist
                console.log("Bar to remove does not exist");
                return;
            }

            var canvas = document.getElementById('bar' + bar_count);
        }

        return {
            append_new_bar : _append_new_bar
        }
    })();

    /*
    * Place Holder
    * */

    /* Register response to events */
    $('#new_bar').click(Editor.append_new_bar);

});

