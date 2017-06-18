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
        var MAX_BARS = 1000;
        var DEFAULT_TABSTAVE = "tabstave notation=true tablature=false";
        var DEFAULT_NOTES = ":w ##";
        var VT_DATA_NAME = "vt_data";

        // Module specific variables
        var composition_id = -1;
        var user_id = -1;
        var bar_count = 0;
        var current_bar = -1;
        var socket = null;

        // For version history
        var save_enabled = true;
        var current_version = true;
        var version_names = [];
        var version_slider = $("#version-slider");

        // List of editable bars as JSON Objects
        var editable_bars = [];

        var DEBUG = false;

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

                _render_append_bar(i);
            }
        }

        function _render_append_bar(bar_id) {
            var canvas = document.createElement("canvas");
            canvas.id = "bar_" + bar_id;
            canvas.setAttribute("class", "bar-block");

            // VexTab JSON String
            var vt_json = document.createElement("div");
            vt_json.id = "vt_" + bar_id;
            vt_json.setAttribute("class", "vex-string-hidden");

            var outer_span = document.createElement("span");
            outer_span.id = "bar_outer_" + bar_id;
            outer_span.setAttribute("class", "canvas-outer");
            outer_span.appendChild(canvas);

            document.getElementById("render_block").appendChild(outer_span);
            document.getElementById("render_block").appendChild(vt_json);

            $("#vt_" + bar_id).data(VT_DATA_NAME, JSON.stringify(editable_bars[bar_id]));
            _rerender_bar(bar_id);

            // Register click event for canvas
            $("#bar_" + bar_id).click(_change_scope);
            bar_count++;
        }

        function _rerender_bar(bar_id) {
            var div_storage = $("#vt_" + bar_id);
            var vt_json_string = div_storage.data(VT_DATA_NAME);
            var vt_json = JSON.parse(vt_json_string);
            var vex_string = _build_vextab(vt_json);
            var canvas = document.getElementById("bar_" + bar_id);
            var canvas_width = {width: canvas.offsetWidth};

            // Render to canvas
            Render.render_bar(bar_id, canvas_width, vex_string);
        }

        /**
         * Accepts a JSON object representing composition
         * Renders it to the canvas block
         * @private
         */
        function _load_init() {
            var render_block = $("#render_block");

            /* Get composition attributes from server */
            // var composition_json;
            $.get(render_block.attr("data-ajax-target"),
                _composition_handler, "json");

            composition_id = render_block.attr("data-composition-id");
            // Ensure that user_id is in fact an int.
            user_id = parseInt(render_block.attr("data-user-id"));

            socket = new WebSocket("ws://" + window.location.host + "/ws_comp/" + composition_id + "/");

            socket.onopen = function() {
                $("#edit_form").submit(Editor.save_bar_click);
                $("#new_bar").click(Editor.send_append_bar);
                $("#version-form").submit(Editor.version_checkout);
                $("#version-save-btn").click(Editor.version_save);
            };
            socket.onmessage = function(e) {
                var data = JSON.parse(e.data);
                if (data.bar_mod === "update") {
                    _update_bar_div(data.bar_id, data.bar_contents)
                } else if (data.bar_mod === "append") {
                    _receive_append_bar(data.bar_contents)
                } else if (data.bar_mod === "select") {
                    if (data.user !== user_id)
                        _oth_user_select(data.bar_id);
                } else if (data.bar_mod === "deselect") {
                    if (data.user !== user_id)
                        $("#bar_outer_" + data.bar_id).removeClass("oth-user");
                } else if (data.bar_mod === "connect_message") {
                    for (var user in data.selection) {
                        // Property check for JS
                        if (data.selection.hasOwnProperty(user)) {
                            _oth_user_select(data.selection[user]);
                        }
                    }
                    version_names = data.version_list;
                    version_slider.attr("max", version_names.length);
                    version_slider.attr("value", version_names.length);
                    version_names.push("Current");
                } else if (data.bar_mod === "delete_last") {
                    var to_remove = bar_count - 1;

                    if (current_bar === bar_count) {
                        // Last bar removed, go to previous
                        current_bar = bar_count - 1;
                    }
                    bar_count--;

                    $("#bar_outer_" + to_remove).remove();
                } else if (data.bar_mod === "version_get") {
                    _load_composition(data.bar_contents);
                } else {
                    console.log("Invalid WebSocket message received, data: " + JSON.stringify(data));
                }
            }
        }

        function _version_name_update(version_id) {
            $("#version-name").html(version_names[version_id]);
        }

        function _version_checkout(event) {
            var version_id = parseInt(version_slider.val());
            _deselect(current_bar);
            current_version = (version_id == version_names.length - 1);

            socket.send(JSON.stringify({
                'action': "version_get",
                'bar_contents': version_id
            }));
            event.preventDefault();
        }

        function _version_save() {
            var comment = $("#version-new-name").val();
            socket.send(JSON.stringify({
                'action': "version_save",
                'bar_contents': comment
            }))
        }

        function _load_composition(bar_list) {
            save_enabled = current_version;
            for (var i = 0; i < bar_list.length; i++) {
                _update_bar_div(i, bar_list[i]);
            }
        }

        function _oth_user_select(bar_id) {
            $("#bar_outer_" + bar_id).addClass("oth-user");
        }

        // Appends a new bar to render block
        function _receive_append_bar(bar_contents) {
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
            editable_bars.push(editable_bar);

            _render_append_bar(bar_count);
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
            if (bar_id >= 0) {
                $("#bar_outer_" + bar_id).removeClass("selected");
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

            // only select bar_id if its not the current_bar
            if (current_bar !== bar_id) {
                // show editor
                $("#toggle-editor").removeClass("collapsed");
                $("#editor-collapse").addClass("in");

                // Highlight the selected canvas
                socket.send(JSON.stringify({
                    'action': "select",
                    'bar_id': bar_id
                }));

                $("#bar_outer_" + bar_id).addClass("selected");

                current_bar = bar_id;

                var vt_json_string = $("#vt_" + bar_id).data(VT_DATA_NAME);
                var vt_json = JSON.parse(vt_json_string);

                // Display vextab notes to editor textbox
                $("#edit_text").val(vt_json["notes"]);
                _rerender_bar(bar_id);

                // Display to user which bar is selected
                $('label[for="edit_text"]').html("Editing Bar " + (bar_id + 1));

                BarComment.retrieve_comments(current_bar);
            } else {
                // hide editor
                $("#toggle-editor").addClass("collapsed");
                $("#editor-collapse").removeClass("in");

                // no bar selected
                current_bar = -1;
                _reset_comments();
            }
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

            socket.send(JSON.stringify({
                'action': "delete_last",
            }));
        }

        function _update_bar_div(bar_id, bar_contents) {
            var div_storage = $("#vt_" + bar_id);
            var vt_json_string = div_storage.data(VT_DATA_NAME);
            var vt_json = JSON.parse(vt_json_string);
            vt_json["notes"] = bar_contents;

            div_storage.data(VT_DATA_NAME, JSON.stringify(vt_json));
            _rerender_bar(bar_id);
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
            if (save_enabled === false) {
                // Can't save
            } else if (bar_id < 0 || bar_id >= editable_bars.length) {
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
                        'bar_id': bar_id,
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

        /* Clear comments when bar is deselected */
        function _reset_comments() {
            $("#total-comments").text("Select Bar");
            $("#comment-block").empty();
            $("#comment_form").addClass("hide");
        }

        /* Initialisation code */

        _load_init();

        return {
            version_checkout: _version_checkout,
            version_name_update: _version_name_update,
            version_save: _version_save,
            send_append_bar: _send_append_bar,
            remove_bar: _remove_bar,
            edit_bar: _edit_bar,
            save_bar_click: _save_bar_click,
            get_bar_count: _get_bar_count,
            get_current_bar: _get_current_bar
        }
    })();

    // insert hint into input at cursor position
    $(".notation-select").click(function(){
        var input_field = $("#edit_text");
        var cursorPos = input_field.prop("selectionStart");
        var v = input_field.val();
        var textBefore = v.substring(0, cursorPos);
        var textAfter  = v.substring(cursorPos, v.length);
        var hint_text = $(this).attr("data-text");
        input_field.val(textBefore + hint_text + textAfter);

        // refocus on text input and make cursor point to where we left off
        input_field.focus();
        var new_pos = cursorPos + hint_text.length;
        input_field[0].selectionStart = new_pos;
        input_field[0].selectionEnd = new_pos;
    });

    /* Register response to events */
    $("#remove_bar").click(Editor.remove_bar);
    $("#edit_text").keyup(_.throttle(Editor.edit_bar, 250));

    // toggle drop-down menu by clicking button
    $('#chat-dropdown-toggle').click(function() {
        $("#chat-dropdown").toggleClass('open');
        // auto-focus on chatbox input
        $("#chat-msg").focus();

        var chat_box = $("#chats");

        // auto scroll to bottom of chat
        chat_box.scrollTop(chat_box[0].scrollHeight);
    });

    // audio playing
    var audio_playback = $("#audio-playback");
    var audio = $("#placeholder-audio")[0];
    var icon = $("#audio-playback").find("span");

    audio_playback.click(function () {
        var play = icon.attr("data-play");
        icon.removeClass();
        if (play === "play") {
            icon.addClass("glyphicon glyphicon-pause");
            audio.play();
            icon.attr("data-play", "pause");
        } else {
            icon.addClass("glyphicon glyphicon-play");
            audio.pause();
            icon.attr("data-play", "play");
        }
    });

    // change back to play button when audio ends
    audio.onended = function() {
        icon.removeClass();
        icon.addClass("glyphicon glyphicon-play");
        icon.attr("data-play", "play");
    };

});
