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
        var current_bar = 0;

        // Appends a new bar to render block
        function _append_new_bar() {
            if (bar_count < MAX_BARS) {
                bar_count++;

                // Add to HTML DOM
                var canvas = document.createElement("canvas");
                canvas.id = "bar" + bar_count;
                canvas.setAttribute("class", "bar-block");
                document.getElementById("render_block").appendChild(canvas);

                // JS/JQUERY Management
                // Bar Object
                var EditableBar = (function () {
                    var bar_number = bar_count;

                    var DEFAULT_TABSTAVE = "tabstave notation=true tablature=false";
                    // Defaults that can be overridden
                    var clef = "none";
                    var time_sig = "";
                    var notes = "";

                    // First bar
                    if (bar_count === 1) {
                        clef = "treble";
                        time_sig = "4/4";
                    }

                    // Canvas to render to
                    var bar_canvas = canvas;

                    function _edit() {
                        console.log("Editing bar: " + bar_number);

                        // Selects this bar to edit
                        _select()
                    }

                    function _select() {
                        // Selects this bar for editing
                        var vex_string = _build_vextab();

                        var bar_canvas_size = {width: bar_canvas.offsetWidth};
                        Render.render_bar(bar_canvas.id, bar_canvas_size, vex_string);
                    }

                    function _build_vextab() {
                        var vex_string = DEFAULT_TABSTAVE;
                        vex_string += " clef=" + clef;

                        if (time_sig !== "") {
                            vex_string += " time=" + time_sig;
                        }

                        vex_string += "\n";

                        if (notes !== "") {
                            vex_string += "notes " + notes + "\n";
                        }

                        return vex_string;
                    }

                    return {
                        edit: _edit
                    }
                })();

                // Register click event
                $("#bar" + bar_count).click(EditableBar.edit);

                EditableBar.edit();
            } else {
                console.log("Maximum bars that can be rendered has been reached.");
            }
        }

        function _remove_bar() {
            if (bar_count === 0) {
                // All compositions must have at least one bar
                console.log("All compositions must have at least a bar!")
                return;
            }

            if (current_bar > bar_count) {
                // Bar does not exist
                console.log("Bar to remove does not exist");
                return;
            }

            var to_remove = current_bar;

            if (current_bar === bar_count) {
                // Last bar removed, go to previous
                current_bar = bar_count - 1;
            }

            $("#bar" + to_remove).remove();
        }

        return {
            append_new_bar: _append_new_bar,
            remove_bar: _remove_bar
        }
    })();

    /*
     * Place Holder
     * */

    /* Register response to events */
    $("#new_bar").click(Editor.append_new_bar);
    $("#remove_bar").click(Editor.remove_bar);

});

