/**
 * Created by andre on 7/1/17.
 */


$(document).ready(function () {

    // создать подключени
    socket = new WebSocket("ws://139.59.155.192/chat/1");

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