var jukebox;
var tabs;

$(function() {
    jukebox = new JukeboxViewModel();
    jukebox.setup();
    refresh();
    tabs = new TabManager();
});

var jsonRpcRequestId = 1;
function rpc(method, params, callback, target) {
    if (!target) {
        target = "jukebox";
    }
    data = {
        method: method,
        params: params,
        id: jsonRpcRequestId++,
        version: "1.1",
    };
    $.ajax("/rpc/" + target, {
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
    if (jukebox.roots.open) {
        refreshRoots();
    }
    setTimeout(refresh, 3000);
}

function showModal(modal, onClose) {
    $('.modalbox').each(function() {
        $(this).hide();
    });
    var closeModal = function() {
        $("#clicktrap").fadeOut();
        if (onClose) {
            onClose();
        }
    };
    modal
        .show()
        .css({ 'margin-left': -$(modal).width()  / 2 })
        .find(".dialog-buttons button").click(closeModal);
    $("#clicktrap").fadeIn();

    return closeModal;
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
