$(function() {
    setupJukebox();
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
    rpc('get_queue', [], updatePlayer);
    rpc('get_volume', [], updateVolume);
    setTimeout(refresh, 3000);
}
