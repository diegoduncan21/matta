/* Project specific Javascript goes here. */
$(document).ready(function() {

    $('#play').click(function(){
        if ($('#play').attr('src') == '/static/images/soundspect_.gif') {
            $('#audio').trigger('pause');
            $('#play').attr('src','/static/images/glyphicons-174-play.png');
            $('#music').css({
              'margin-left':'13px',
              'bottom': '3px'
            });
            console.log("pausa");
        } else {
            $('#audio').trigger('play');
            $('#play').attr('src','/static/images/soundspect_.gif');
            $('#music').css({
              'margin-left':'0px',
              'bottom': '36px'
            });
            console.log("play");
        }
    });

});
