$(function () {
    var vt = VexTabDiv;
    var VexTab = vt.VexTab;
    var Artist = vt.Artist;
    var Renderer = Vex.Flow.Renderer;

    // Remove "vexflow.com" logo that is rendered by default
    Artist.NOLOGO = true;
    VexTab.DEBUG = false;

    // Create VexFlow Renderer from canvas element with id #canvas-to-load
    var renderer = new Renderer($('#canvas-to-load')[0], Renderer.Backends.CANVAS);

    // Initialize VexTab artist and parser.
    var artist = new Artist(10, 10, 600, {scale: 0.8});
    var vextab = new VexTab(artist);

    function render() {
        try {
            vextab.reset();
            artist.reset();
            vextab.parse($("#to-render").val());
            artist.render(renderer);
            $("#error").text("");
        } catch (e) {
            console.log(e);
            $("#error").html(e.message.replace(/[\n]/g, '<br/>'));
        }
    }

    $("#to-render").keyup(_.throttle(render, 250));
    render();
});
