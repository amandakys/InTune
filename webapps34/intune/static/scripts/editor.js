$(document).ready(function () {
    // Module specific constants
    var MAX_BARS = 5;

    // Module specific variables
    var bar_count = 0;



    // Appends a new bar to render block
    window.new_bar = function add_new() {
        if (bar_count < MAX_BARS) {
            bar_count++;
            var canvas = document.createElement('canvas');
            canvas.id = "bar" + bar_count;
            canvas.setAttribute("class", "bar-block");
            document.getElementById('render_block').appendChild(canvas);

            var canvas_size = {width: canvas.offsetWidth};
            Render.render_bar(canvas.id, canvas_size, "");
        } else {
            console.log("Maximum bars that can be rendered has been reached.");
        }

    }

});

