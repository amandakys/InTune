$(document).ready(function () {
    // Module specific constants
    var MAX_BARS = 5;

    // Module specific variables
    var bar_count = 0;

    var getCookie = function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    var csrftoken = getCookie('csrftoken');
    var csrfSafeMethod = function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Appends a new bar to render block
    window.new_bar = function add_new() {
        // $.ajax({
        //         method: "POST",
        //         url: "",
        //         dataType: "json",
        //         encode: true
        //     }
        // );

        // Scale according to dimensions of render block

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

