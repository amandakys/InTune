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
        var DEFAULT_TABSTAVE = "tabstave notation=true tablature=false";
        var VT_DATA_NAME = "vt_data";

        // Module specific variables
        var bar_count = 0;
        var current_bar = 0;

        // List of editable bars as JSON Objects
        var editable_bars = [];

        function _composition_handler(data) {
            // Debug Statement
            var json_string = JSON.stringify(data);
            console.log("Composition data:\n" + json_string);

            var bars = data["bars"];
            var size = bars.length;

            for (var i = 0; i < size; i++) {
                if (bar_count >= MAX_BARS) {
                    console.log("Max number of bars that can be rendered reached");
                    return;
                }

                console.log("Bar [" + i + "]: " + bars[i]);
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

                // console.log(JSON.stringify(vt_json));
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

            document.getElementById("render_block").appendChild(canvas);
            document.getElementById("render_block").appendChild(vt_json);

            $("#vt_" + canvas_no).data(VT_DATA_NAME,
                JSON.stringify(editable_bars[canvas_no]));

            var vex_string = _build_vextab(bar_json);
            var canvas_width = {width: canvas.offsetWidth};
            // console.log("canvas_width: " + canvas_width.width);
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
        }

        // Appends a new bar to render block
        function _append_new_bar() {
            if (bar_count < MAX_BARS) {
                // Add to HTML DOM
                // Canvas
                var canvas = document.createElement("canvas");
                canvas.id = "bar_" + bar_count;
                canvas.setAttribute("class", "bar-block");
                // VexTab JSON String
                var vt_json = document.createElement("div");
                vt_json.id = "vt_" + bar_count;
                vt_json.setAttribute("class", "vex-string-hidden");

                document.getElementById("render_block").appendChild(canvas);
                document.getElementById("render_block").appendChild(vt_json);

                // Default JSON Object (representing VexTab) for new bar
                var editable_bar = {};
                editable_bar["options"] = "";
                editable_bar["tabstave"] = DEFAULT_TABSTAVE;
                if (bar_count === 1) {
                    // First bar
                    editable_bar["clef"] = "treble";
                    editable_bar["time_sig"] = "4/4";
                } else {
                    editable_bar["clef"] = "none";
                    editable_bar["time_sig"] = "";
                }
                editable_bar["notes"] = "";

                $("#vt_" + bar_count).data(VT_DATA_NAME, JSON.stringify(editable_bar));
                editable_bars.push(editable_bar);

                _select(bar_count);

                // Register click event for canvas
                $("#bar_" + bar_count).click(_change_scope);

                // Update server about new bar
                $.ajax({
                    method: "POST",
                    url: $("#new_bar").attr("data-ajax-target"),
                    dataType: "json",
                    encode: true
                });

                bar_count++;
            } else {
                console.log("Maximum bars that can be rendered has been reached.");
            }
        }

        /**
         * Takes an INTEGER bar_id and makes the bar corresponding to this id to
         * be the current editing scope
         * @param bar_id
         * @private
         */
        function _select(bar_id) {
            current_bar = bar_id;

            // console.log("Selecting: " + "vt_" + bar_id);
            var vt_json_string = $("#vt_" + bar_id).data(VT_DATA_NAME);
            // console.log("vt_json_string: " + vt_json_string);
            var vt_json = JSON.parse(vt_json_string);

            var vex_string = _build_vextab(vt_json);
            // console.log("vexstring: " + vex_string);

            // Display vextab notes to editor textbox
            $("#bar_notes").val(vt_json["notes"]);

            // Render to canvas
            var canvas = document.getElementById("bar_" + bar_id);
            var canvas_width = {width: canvas.offsetWidth};
            // console.log("canvas_width: " + canvas_width.width);
            Render.render_bar("bar_" + bar_id, canvas_width, vex_string);
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
            console.log("Select Bar: " + this.id);
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

            $("#bar" + to_remove).remove();
        }

        function _edit_bar() {
            console.log("Edit Bar: " + current_bar);
            if (current_bar < 0) {
                console.log("No Bar to edit!");
                return;
            }

            var div_storage = $("#vt_" + current_bar);
            var vt_json_string = div_storage.data(VT_DATA_NAME);

            var vt_json = JSON.parse(vt_json_string);
            vt_json["notes"] = $("#bar_notes").val();

            // vt_json_string = JSON.stringify(vt_json);
            // console.log("vt_json_string: " + vt_json_string);

            var vex_string = _build_vextab(vt_json);
            // Render to canvas
            var canvas = document.getElementById("bar_" + current_bar);
            var canvas_width = {width: canvas.offsetWidth};
            // console.log("canvas_width: " + canvas_width.width);
            Render.render_bar("bar_" + current_bar, canvas_width, vex_string);

            // Update data in div
            div_storage.data(VT_DATA_NAME, JSON.stringify(vt_json));
        }

        function _save_bar(event) {
            if (current_bar < 0 || current_bar >= editable_bars.length) {
                // Verify valid bar
                $("#save_error").html("Please select a bar to edit!");
            } else if ($("#edit_error").html().length > 0) {
                // Verify no compile errors
                $("#save_error").html("Can't save invalid bar!");
            } else {
                var form = $("#edit_form");

                // Specify the bar, composition id
                var form_data = {
                    'composition_id': form.attr('data-composition-id'),
                    'bar_id': current_bar,
                    'bar_contents': $("#bar_notes").val()
                };
                // Submit
                $.ajax({
                    type: form.attr('method'),
                    url: form.attr('action'),
                    data: form_data,
                    dataType: "json",
                    encode: true
                }).done(function(result) {
                    console.log(result);
                });
            }
            event.preventDefault();
        }

        /* Initialisation code */

        _load_init();

        return {
            append_new_bar: _append_new_bar,
            remove_bar: _remove_bar,
            edit_bar: _edit_bar,
            save_bar: _save_bar
        }
    })();

    /* Register response to events */
    $("#new_bar").click(Editor.append_new_bar);
    $("#remove_bar").click(Editor.remove_bar);
    $("#bar_notes").keyup(_.throttle(Editor.edit_bar, 250));
    $("#edit_form").submit(Editor.save_bar);
});
