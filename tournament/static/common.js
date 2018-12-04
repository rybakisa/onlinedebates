$(document).ready(function () {

    $('.block-round-info__round-number').click(function () {
        var tab_id = $(this).attr('data-tab');
        $('.block-round-info__round-number').removeClass('block-round-info__round-number--active');

        $('.block-round-info__body').removeClass('block-round-info--active');

        $(this).addClass('block-round-info__round-number--active');
        $("#" + tab_id).addClass('block-round-info--active');
    })

})

$(document).ready(function () {
    $(".page-header__schedule").click(function () {
        $(".page-header__schedule-container").slideToggle();
    });
    $(".page-header__smoke-rooms-title").click(function () {
        $(".page-header__smoke-room-container").slideToggle();
    });
    $("#moscow-title").hover(function () {
        $("#moscow").toggle();
    });
    $("#ekb-title").hover(function () {
        $("#ekb").toggle();
    });
    $("#omsk-title").hover(function () {
        $("#omsk").toggle();
    });
    $("#nsk-title").hover(function () {
        $("#nsk").toggle();
    });
    $("#vdk-title").hover(function () {
        $("#vdk").toggle();
    });
});