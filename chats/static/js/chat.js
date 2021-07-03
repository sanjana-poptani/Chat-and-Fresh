var text_box = '<div class="row message-body">' +
    '<div class="col-sm-12 message-main-sender"><div class="sender">{sender}</div></div>' +
    '<div class="message-text">{message}</div>' +
    '</div>';

function scrolltoend() {
    $('#conversation').stop().animate({
        scrollTop: $('#conversation')[0].scrollHeight
    }, 800);
}

function ChooseImage() {
    document.getElementById('imageFile').click();
}

function send(sender, receiver, message) {
    $.post('/api/messages/', '{"sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }', function(data) {
        console.log(data);
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#conversation').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/api/messages/' + sender_id + '/' + receiver_id, function(data) {
        console.log(data);
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('#conversation').append(box);
                scrolltoend();
            }
        }
    })
}