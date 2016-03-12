/* Project specific Javascript goes here. */
$(document).ready(function() {

    $('#play').click(function(){
        if ($('#play').attr('src') == '/static/images/soundspect_.gif') {
            $('#audio').trigger('pause');
            $('#play').attr('src','/static/images/glyphicons-174-play.png');
            console.log("pausa");
        } else {
            $('#audio').trigger('play');
            $('#play').attr('src','/static/images/soundspect_.gif');
            console.log("play");
        }
    });

});
