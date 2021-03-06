/**
 * Module "Render":
 * + render_bar
 * - _render_bar
 */
var Render = (function () {
    "use strict";

    // Constants
    var DEFAULT_OPTIONS = "";
    var DEFAULT_STAVE = "tabstave notation=true tablature = false";

    function _render_bar(canvas_id, canvas_size, vex_string) {
        var vt = VexTabDiv;
        var VexTab = vt.VexTab;
        var Artist = vt.Artist;
        var Renderer = vt.Flow.Renderer;

        // Remove "vexflow.com" logo that is rendered by default
        Artist.NOLOGO = true;
        vt.DEBUG = false;

        // Create VexFlow Renderer from canvas element with id #boo.
        var renderer = new Renderer("bar_" + canvas_id, Renderer.Backends.CANVAS);

        var artist = new Artist(0, 0, canvas_size.width);
        var vextab = new VexTab(artist);

        try {
            vextab.reset();
            artist.reset();

            if (vex_string === "") {
                vex_string = DEFAULT_OPTIONS + DEFAULT_STAVE;
            }
            vextab.parse(vex_string);
            artist.render(renderer);
            $("#edit_error").text("");
            $("#bar_outer_" + canvas_id).removeClass("render-error");
        } catch (e) {
            $("#edit_error").html(e.message.replace(/[\n]/g, "<br/>"));
            $("#bar_outer_" + canvas_id).addClass("render-error");
        }
    }

    function _syntax_verify(notes) {
        var vt = VexTabDiv;
        var VexTab = vt.VexTab;
        var Artist = vt.Artist;
        var artist = new Artist(0, 0, 200);
        var vextab = new VexTab(artist);

        try {
            vextab.reset(); artist.reset();
            vextab.parse(notes);
            return true;
        } catch (e) {
            console.log(e);
            return false;
        }
    }

    return {
        render_bar: _render_bar,
        syntax_verify: _syntax_verify
    }

})();
