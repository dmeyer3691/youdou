(function() {

$(document).ready(function() {
  $(".video-wrapper").fitVids();

  $(".ask-watson").click(function() {
    $(".site-content").fadeOut('slow');
    $(".watson-thinking").fadeIn('slow');
  });

});

})();

