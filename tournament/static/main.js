/**
 * Created by andre on 7/1/17.
 */


$(document).ready(function () {

    // создать подключени
    socket = new WebSocket(((window.location.protocol == 'http:') ? 'ws://':'wss://') +  window.location.host + '/chat/1');

    // Это чтобы текущее статус не ломался при перезагрузке страницы (например, выводить страницу фидбэка)
    // а также для того, чтобы запустить таймер при начале раунда, так как при событии start_round с web-socket-а
    // мы просто перезагружаем страницу
    var server_page_status = $('meta[name=server_page_status]').attr("content");
    if (server_page_status == 'preparing') {

        client_status = Cookies.get('client_status');
        time_remaining = Cookies.get('time_remaining');
        countDownDate = new Date();

        if (client_status == undefined) {
            Cookies.set('client_status', 'preparing');
            // 15 минут = 900 sec
            Cookies.set('time_remaining', 900);
            // брать значение в sec из кукисов и прибавлять к текущему времени,
            countDownDate.setMinutes(countDownDate.getMinutes() + 15);
        }
        else if (client_status == 'preparing') {
            // звуковой сигнал
            // достать из кукисов оставшееся время подготовки
            tr = Cookies.get('time_remainig');
            // если его нет, то постаивить 15 минут
            if (tr == undefined) {
                Cookies.set('time_remaining', 15);
            }
            // продолжение отсчета
            else {
                countDownDate.setSeconds(countDownDate.getSeconds() + tr);
            }
        }
        else if (client_status == 'on_round') {
            // вроде бы ничего не надо делать
        }
        // + проверить куку со статусом (если waiting_for_feedback то показываем модалку
        else if (client_status == 'waiting_for_feedback') {
            // показать модальное окно
        }

    }
    else if (server_page_status == 'waiting_for_feedback') {
        // показать модальное окно
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
        }
        else if (parsedData.event == "start_round") {
            location.reload();
        }
        // чтобы отодвигать время начала
        else if (parsedData.event == "set_round_start_time") {
            // TODO: отправлять с сервера на время начала, а через сколько начнется
            var countDownDate = new Date(parsedData.data.start_time).getTime();
        }
        else if (parsedData.event == "get_feedback") {
            // вывести модально окно
            // мета статуса в значение waiting_for_feedback
        }
    };

    // отправить сообщение
    $(".block-chat__button-send").click(function () {
        messageFrom = $('meta[name=user_id]').attr("content");
        messageText = $(".block-chat__input").val();
        messageJson = '{"event":"chat", "data":{"from_id":"' + messageFrom + '", "text":"' + messageText + '"}}';
        socket.send(messageJson);
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
            nameStyle = '<span class="block-chat__name block-chat__name--username">' + from_name + '</span>'; }
        else { nameStyle = '<span class="block-chat__name">' + from_name + '</span>'; }

        messageElem = '<div class="block-chat__message"><div class="block-chat__msg-first-line">' +
            nameStyle + '<span class="block-chat__date">' + time + '</span></div><span class="block-chat__text">' +
            message + '</span></div>';
        $(".block-chat__scrolling-part").append(messageElem);
    }

});