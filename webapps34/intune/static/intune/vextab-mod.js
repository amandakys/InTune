$(function () {
    var vt = VexTabDiv;
    var VexTab = vt.VexTab;
    var Artist = vt.Artist;
    var Renderer = vt.Flow.Renderer;

    // Remove "vexflow.com" logo that is rendered by default
    Artist.NOLOGO = true;
    vt.DEBUG = false;

    // Create VexFlow Renderer from canvas element with id #boo.
    var renderer = new Renderer($('#canvas-to-load2')[0], Renderer.Backends.CANVAS);

    var artist = new Artist(10, 10, 600, {scale: 1});
    var vextab = new VexTab(artist);

    function render2() {
        try {
            vextab.reset();
            artist.reset();
            var staff_text = $("#staff-prop").val().concat("\r\n");
            var notes_text = $("#notes").val();
            // Only add notes if the textarea for it is not empty
            if ($.trim(notes_text)) {
                notes_text = "notes " + notes_text + "\r\n";
            }
            var full = staff_text.concat(notes_text);
            // $("#ECHO").text(full.replace(/[\r\n]/g, '<br/>'));
            vextab.parse(full);
            artist.render(renderer);
            $("#error2").text("");
        } catch (e) {
            console.log(e);
            $("#error2").html(e.message.replace(/[\n]/g, "<br/>"));
        }
    }

    $("#notes").keyup(_.throttle(render2, 250));
    render2();
});
