$(document).ready(function () {
    // Enforce module to load only when DOM is ready

    /**
     * Editor Module
     * Support operations are listed in "@type"
     * Remaining functions are declared "private" and should not be used
     * outside of this module!
     *
     * Refactor_2: Refactoring may be needed to remove excessive duplication,
     * especially in _composition_handler and _append_bar
     *
     * @type {{send_append_bar, remove_bar, edit_bar, save_bar, get_bar_count
     *          get_current_bar}}
     */
    window.Editor = (function () {
        "use strict";
        // Module specific constants
        var MAX_BARS = 5;
        var DEFAULT_TABSTAVE = "tabstave notation=true tablature=false";
        var DEFAULT_NOTES = ":w ##";
        var VT_DATA_NAME = "vt_data";

        // Module specific variables
        var composition_id = -1;
        var bar_count = 0;
        var current_bar = 0;
        var socket = null;

        // List of editable bars as JSON Objects
        var editable_bars = [];

        var DEBUG = true;

        function _debug_log(msg) {
            if (DEBUG) console.log(msg);
        }

        function _composition_handler(data) {
            // Debug Statement
            var json_string = JSON.stringify(data);
            _debug_log("Composition data:\n" + json_string);

            var bars = data["bars"];
            var size = bars.length;

            for (var i = 0; i < size; i++) {
                if (bar_count >= MAX_BARS) {
                    console.log("Max number of bars that can be rendered reached");
                    return;
                }

                _debug_log("Bar [" + i + "]: " + bars[i]);
                // JSON Object representing vt string
                // Repackaging required as data model does not contain every
                // required information
                var editable_bar = {};
                editable_bar["options"] = "";
                editable_bar["tabstave"] = DEFAULT_TABSTAVE;
                if (i === 0) {
                    // First bar
                    editable_bar["clef"] = "treble";
                    editable_bar["time_sig"] = "4/4";
                } else {
                    editable_bar["clef"] = "none";
                    editable_bar["time_sig"] = "";
                }
                editable_bar["notes"] = bars[i];
                editable_bars.push(editable_bar);

                _render_bar(editable_bar, i);

                bar_count++;
            }
        }

        function _render_bar(bar_json, canvas_no) {
            var canvas = document.createElement("canvas");
            canvas.id = "bar_" + canvas_no;
            canvas.setAttribute("class", "bar-block");
            // VexTab JSON String
            var vt_json = document.createElement("div");
            vt_json.id = "vt_" + canvas_no;
            vt_json.setAttribute("class", "vex-string-hidden");

            var outer_span = document.createElement("span");
            outer_span.id = "bar_outer_" + canvas_no;
            outer_span.setAttribute("class", "canvas-outer");
            outer_span.appendChild(canvas);

            document.getElementById("render_block").appendChild(outer_span);
            document.getElementById("render_block").appendChild(vt_json);

            $("#vt_" + canvas_no).data(VT_DATA_NAME,
                JSON.stringify(editable_bars[canvas_no]));

            var vex_string = _build_vextab(bar_json);
            var canvas_width = {width: canvas.offsetWidth};
            Render.render_bar(canvas.id, canvas_width, vex_string);

            // Register click event for canvas
            $("#bar_" + canvas_no).click(_change_scope);
        }

        /**
         * Accepts a JSON object representing composition
         * Renders it to the canvas block
         * @private
         */
        function _load_init() {
            /* Get composition attributes from server */
            // var composition_json;
            $.get($("#render_block").attr("data-ajax-target"),
                _composition_handler, "json");

            composition_id = $("#render_block").attr("data-composition-id");
            socket = new WebSocket("ws://" + window.location.host + "/ws_comp/" + composition_id + "/");

            socket.onopen = function() {
                $("#edit_form").submit(Editor.save_bar_click);
                $("#new_bar").click(Editor.send_append_bar);
            };
            socket.onmessage = function(e) {
                var data = JSON.parse(e.data);
                if (data.bar_mod == "update") {
                    _update_bar_div(data.bar_id, data.bar_contents)
                } else if (data.bar_mod == "append") {
                    _receive_append_bar(data.bar_contents)
                } else {
                    console.log("Invalid WebSocket message received");
                }
            }
        }

        // Appends a new bar to render block
        function _receive_append_bar(bar_contents) {
            // Add to HTML DOM
            // Canvas
            var canvas = document.createElement("canvas");
            canvas.id = "bar_" + bar_count;
            canvas.setAttribute("class", "bar-block");
            // VexTab JSON String
            var vt_json = document.createElement("div");
            vt_json.id = "vt_" + bar_count;
            vt_json.setAttribute("class", "vex-string-hidden");

            var outer_span = document.createElement("span");
            outer_span.id = "bar_outer_" + bar_count;
            outer_span.setAttribute("class", "canvas-outer");
            outer_span.appendChild(canvas);

            document.getElementById("render_block").appendChild(outer_span);
            document.getElementById("render_block").appendChild(vt_json);

            // Default JSON Object (representing VexTab) for new bar
            var editable_bar = {};
            editable_bar["options"] = "";
            editable_bar["tabstave"] = DEFAULT_TABSTAVE;
            if (bar_count === 0) {
                // First bar
                editable_bar["clef"] = "treble";
                editable_bar["time_sig"] = "4/4";
            } else {
                editable_bar["clef"] = "none";
                editable_bar["time_sig"] = "";
            }
            editable_bar["notes"] = bar_contents;

            $("#vt_" + bar_count).data(VT_DATA_NAME, JSON.stringify(editable_bar));
            editable_bars.push(editable_bar);

            var vt_json_string = $("#vt_" + bar_count).data(VT_DATA_NAME);
            var vt_json_notes = JSON.parse(vt_json_string);
            var vex_string = _build_vextab(vt_json_notes);

            // Render to canvas
            var canvas_width = {width: canvas.offsetWidth};
            Render.render_bar("bar_" + bar_count, canvas_width, vex_string);

            // Register click event for canvas
            $("#bar_" + bar_count).click(_change_scope);

            bar_count++;
        }

        // Sends instruction to append bar to the server
        function _send_append_bar() {
            if (bar_count < MAX_BARS) {
                socket.send(JSON.stringify({
                    'action': "append",
                    'bar_contents': DEFAULT_NOTES
                }));
            } else {
                console.log("Maximum bars that can be rendered has been reached.");
            }
        }

        function _deselect(bar_id) {
            if (bar_id > 0) {
                $("#bar_outer_" + current_bar).attr("class", "canvas-outer");
                _save_bar(bar_id);
            }
        }

        /**
         * Takes an INTEGER bar_id and makes the bar corresponding to this id to
         * be the current editing scope
         * @param bar_id
         * @private
         */
        function _select(bar_id) {
            // Deselect the previous canvas
            _deselect(current_bar);
            // Highlight the selected canvas
            $("#bar_outer_" + bar_id).attr("class", "selected canvas-outer");

            current_bar = bar_id;

            var vt_json_string = $("#vt_" + bar_id).data(VT_DATA_NAME);
            var vt_json = JSON.parse(vt_json_string);

            var vex_string = _build_vextab(vt_json);

            // Display vextab notes to editor textbox
            $("#edit_text").val(vt_json["notes"]);

            // Render to canvas
            var canvas = document.getElementById("bar_" + bar_id);
            var canvas_width = {width: canvas.offsetWidth};
            Render.render_bar("bar_" + bar_id, canvas_width, vex_string);

            // Display to user which bar is selected
            $('label[for="edit_text"]').html("Editing Bar " + (bar_id + 1));

            BarComment.retrieve_comments(current_bar);
        }

        function _build_vextab(json) {
            var vex_string = json["options"] + "\n";
            vex_string += json["tabstave"];

            if (json["clef"] !== ""){
                vex_string += " clef=" + json["clef"];
            }

            if (json["time_sig"] !== "") {
                vex_string += " time=" + json["time_sig"];
            }

            vex_string += "\n";

            if (json["notes"] !== "") {
                vex_string += "notes " + json["notes"];
            }

            return vex_string;
        }

        function _change_scope() {
            _debug_log("Select Bar: " + this.id);
            var id = this.id;
            id = id.replace("bar_", "");
            id = parseInt(id);
            _select(id);
        }

        function _remove_bar() {
            if (bar_count === 0) {
                // All compositions must have at least one bar
                console.log("All compositions must have at least a bar!");
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

            $("#bar_" + to_remove).remove();
        }

        function _update_bar_div(bar_id, bar_contents) {
            var div_storage = $("#vt_" + bar_id);
            var vt_json_string = div_storage.data(VT_DATA_NAME);

            var vt_json = JSON.parse(vt_json_string);
            vt_json["notes"] = bar_contents;

            var vex_string = _build_vextab(vt_json);
            // Render to canvas
            var canvas = document.getElementById("bar_" + bar_id);
            var canvas_width = {width: canvas.offsetWidth};
            Render.render_bar("bar_" + bar_id, canvas_width, vex_string);

            // Update data in div
            div_storage.data(VT_DATA_NAME, JSON.stringify(vt_json));
        }

        function _edit_bar() {
            _debug_log("Edit Bar: " + current_bar);
            if (current_bar < 0) {
                console.log("No Bar to edit!");
                return;
            }

            _update_bar_div(current_bar, $("#edit_text").val());
        }

        function _save_bar(bar_id) {
            if (bar_id < 0 || bar_id >= editable_bars.length) {
                // Verify valid bar
                $("#save_error").html("Please select a bar to edit!");
            } else {
                var div_storage = $("#vt_" + bar_id);
                var vt_json_string = div_storage.data(VT_DATA_NAME);
                var vt_json = JSON.parse(vt_json_string);
                var vex_string = _build_vextab(vt_json);

                if (Render.syntax_verify(vex_string)) {
                    // Submit
                    socket.send(JSON.stringify({
                        'action': "update",
                        'bar_id': current_bar,
                        'bar_contents': vt_json["notes"]
                    }));
                } else {
                    console.log("Failed to validate bar contents");
                }
            }
        }

        function _save_bar_click(event) {
            _save_bar(current_bar);
            event.preventDefault();
        }

        function _get_bar_count() {
            return bar_count;
        }

        function _get_current_bar() {
            return current_bar;
        }

        /* Initialisation code */

        _load_init();

        return {
            send_append_bar: _send_append_bar,
            remove_bar: _remove_bar,
            edit_bar: _edit_bar,
            save_bar_click: _save_bar_click,
            get_bar_count: _get_bar_count,
            get_current_bar: _get_current_bar
        }
    })();

    /* Register response to events */
    $("#remove_bar").click(Editor.remove_bar);
    $("#edit_text").keyup(_.throttle(Editor.edit_bar, 250));
});
