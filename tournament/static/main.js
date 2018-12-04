/**
 * Created by andre on 7/1/17.
 */


$(document).ready(function () {

    // создать подключени
    socket = new WebSocket(((window.location.protocol == 'http:') ? 'ws://' : 'wss://') + window.location.host + '/chat/1');


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
            if ($('meta[name=server_page_status]').attr("content") == "waiting_for_round") {
                $(".page-header__timer-watch").text("Раунд вот-вот начнется!");
            } else if ($('meta[name=server_page_status]').attr("content") == "preparing") {
                // звуковой сигнал
                var audio = document.getElementById('audio');
                audio.play();
                $(".page-header__timer-watch").text("Игра началась!");
                Cookies.set('client_status', 'on_round');
            }

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

    // Это чтобы текущее статус не ломался при перезагрузке страницы (например, выводить страницу фидбэка)
    // а также для того, чтобы запустить таймер при начале раунда, так как при событии start_round с web-socket-а
    // мы просто перезагружаем страницу
    var server_page_status = $('meta[name=server_page_status]').attr("content");
    if (server_page_status == 'preparing') {

        client_status = Cookies.get('client_status');
        time_remaining = Cookies.get('time_remaining');

        if (client_status == undefined) {
            Cookies.set('client_status', 'preparing');
            // 15 минут = 900 sec
            Cookies.set('time_remaining', 900);
            // брать значение в sec из кукисов и прибавлять к текущему времени,
            distance = 900;
            var audio = document.getElementById('audio');
            audio.play();
        } else if (client_status == 'preparing') {
            // звуковой сигнал
            var audio = document.getElementById('audio');
            audio.play();
            // достать из кукисов оставшееся время подготовки
            tr = Cookies.get('time_remaining');
            // если его нет, то постаивить 15 минут
            if (tr == undefined) {
                Cookies.set('time_remaining', 900);
                distance = 900;
            }
            // продолжение отсчета
            else {
                distance = tr;
            }
        } else if (client_status == 'on_round') {
            // вроде бы ничего не надо делать
        }
        // + проверить куку со статусом (если waiting_for_feedback то показываем модалку
        else if (client_status == 'waiting_for_feedback') {
            // показать модальное окно
            $(".modal-window").css("display", "flex");
        }
    } else if (server_page_status == 'waiting_for_feedback') {
        // показать модальное окно
        $(".modal-window").css("display", "flex");
    } else if (server_page_status == 'waiting_for_round') {
        Cookies.remove('time_remaining');
        Cookies.remove('client_status');
    }


    // обработчик входящих сообщений
    socket.onmessage = function (event) {
        incomingJson = event.data;
        parsedData = JSON.parse(incomingJson);
        if (parsedData.event == "chat") {
            from_name = parsedData.data.from_name;
            from_id = parsedData.data.from_id;
            time = parsedData.data.time;
            message = parsedData.data.text;
            showMessage(from_name, from_id, time, message);
            $(".block-chat__input").val("");
        } else if (parsedData.event == "start_round") {
            Cookies.remove('time_remaining');
            Cookies.remove('client_status');
            location.reload();
        }
        // чтобы отодвигать время начала
        else if (parsedData.event == "set_round_start_time") {
            // TODO: отправлять с сервера на время начала, а через сколько начнется
            distance = parseInt(parsedData.data.remainig);
        } else if (parsedData.event == "get_feedback") {
            // вывести модально окно
            // мета статуса в значение waiting_for_feedback
            $('meta[name=server_page_status]').attr("content", "waiting_for_feedback");
            $(".modal-window").css("display", "flex");
        }
    };

    // отправить сообщение
    $(".block-chat__button-send").click(function () {
        messageFrom = $('meta[name=user_id]').attr("content");
        messageText = $(".block-chat__input").val();
        messageJson = '{"event":"chat", "data":{"from_id":"' + messageFrom + '", "text":"' + messageText + '"}}';
        if (messageText != '') {
            socket.send(messageJson);
        }
    });

    $(".block-chat__input").keypress(function (e) {
        if (e.which == 13) {
            $(".block-chat__button-send").click();
        }
    });

    // показать сообщение
    function showMessage(from_name, from_id, time, message) {
        var cur_user_id = $('meta[name=user_id]').attr("content");
        if (from_id == cur_user_id) {
            nameStyle = '<span class="block-chat__name block-chat__name--username">' + from_name + '</span>';
        } else {
            nameStyle = '<span class="block-chat__name">' + from_name + '</span>';
        }

        messageElem = '<div class="block-chat__message"><div class="block-chat__msg-first-line">' +
            nameStyle + '<span class="block-chat__date">' + time + '</span></div><span class="block-chat__text">' +
            message + '</span></div>';
        $(".block-chat__scrolling-part").append(messageElem);
    }

});