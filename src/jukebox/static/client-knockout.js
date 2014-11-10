var jukebox;

$(function() {
    jukebox = new JukeboxViewModel();
    jukebox.setup();
    refresh();
});

var jsonRpcRequestId = 1;
function rpc(method, params, callback) {
    data = {
        method: method,
        params: params,
        id: jsonRpcRequestId++,
        version: "1.1",
    };
    $.ajax("/rpc/jukebox", {
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        type: 'POST',
        success: function(result) {
            if (callback) {
                callback(result.result);
            }
        }
    });
}

function refresh() {
    rpc('get_queue', [], updateJukebox);
    rpc('get_volume', [], updateVolume);
    setTimeout(refresh, 3000);
}

function showModal(modal) {
    $('.modalbox').each(function() {
        $(this).hide()
               .css({
            'margin-left': -$(this).width() / 2,
            'margin-top': -$(this).height() / 2,
        });
    });
    modal.show();
    $("#clicktrap").fadeIn();

    return function() {
        $("#clicktrap").fadeOut();
    }
}
