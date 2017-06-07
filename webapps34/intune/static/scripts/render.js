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
        var renderer = new Renderer(canvas_id, Renderer.Backends.CANVAS);

        var artist = new Artist(0, 0, canvas_size.width);
        var vextab = new VexTab(artist);

        try {
            vextab.reset();
            artist.reset();

            if (vex_string === "") {
                vex_string = DEFAULT_OPTIONS + DEFAULT_STAVE;
            }
            // console.log("Parsing:\n" + vex_string);
            vextab.parse(vex_string);
            artist.render(renderer);
            $("#error2").text("");
        } catch (e) {
            console.log(e);
            $("#error2").html(e.message.replace(/[\n]/g, "<br/>"));
        }
    }

    return {
        render_bar: _render_bar
    }

})();
