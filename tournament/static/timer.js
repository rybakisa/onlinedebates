// Set the date we're counting down to
$(document).ready(function () {


    var distance = $('meta[name=next_round_start_time]').attr("content");
    distance = parseInt(distance);

// Update the count down every 1 second
    var x = setInterval(function () {

        distance -= 1;

        // Time calculations for days, hours, minutes and seconds
        var hours = Math.floor((distance % (60 * 60 * 24)) / (60 * 60));
        var minutes = Math.floor((distance % (60 * 60)) / (60));
        var seconds = Math.floor(distance % (60));

        // Display the result
        // If the count down is finished, write some text

        // TODO: по окончании 15 минут звуковой сигнал
        // TODO: и установить куку со статусом в значение on_round
        // TODO: проверять куку состояния!
        if (distance < 0) {
            clearInterval(x);
            $(".page-header__timer-watch").text("Раунд вот-вот начнется!")
        } else {
            $(".page-header__timer-watch").text(hours + ":" + minutes + ":" + seconds);
            // TODO: сохранять в куку каждые N секунд
            if ((seconds % 15 == 0) &&
                ($('meta[name=server_page_status]').attr("content") == 'preparing') &&
                (Cookies.get('client_status') == 'preparing')) {
                Cookies.set('time_remaining', minutes * 60 + seconds);
            }
        }
    }, 1000);
});
