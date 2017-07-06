$(document).ready(function() {
  $(".page-header__schedule").click(function() {
    $(".page-header__schedule-container").slideToggle();
  });
  $(".page-header__smoke-rooms-title").click(function() {
    $(".page-header__smoke-room-container").slideToggle();
  });
  $("#moscow-title").hover(function() {
    $("#moscow").toggle();
  });
  $("#ekb-title").hover(function() {
    $("#ekb").toggle();
  });
  $("#omsk-title").hover(function() {
    $("#omsk").toggle();
  });
  $("#nsk-title").hover(function() {
    $("#nsk").toggle();
  });
  $("#vdk-title").hover(function() {
    $("#vdk").toggle();
  });
});
