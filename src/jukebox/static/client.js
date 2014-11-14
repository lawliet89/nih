var jukebox;
var tabs;

$(function() {
    jukebox = new JukeboxViewModel();
    jukebox.setup();
    refresh();
    tabs = new TabManager();
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

function TabManager() {
    var me = this;
    this.select = function(selector) {
        var previous = $("#tabs li.selected");
        previous.removeClass("selected");
        $(previous.data("content")).hide();

        var newTab = $("#tabs " + selector);
        newTab.addClass("selected");
        $(newTab.data("content")).show();        
    };
    $("#tabs li.queue").click(function() { 
        me.select(".queue"); 
    });
    this.select(".queue"); 
}
