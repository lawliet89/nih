function QueueItem(item, info, queue) {
    this.queue = queue;

    this.id  = ko.observable(item.id);
    this.who = ko.observable(item.username);
    this.url = ko.observable(item.url);

    this.trackName   = ko.observable(info.trackName);
    this.trackNumber = ko.observable(info.trackNumber);
    this.albumTitle  = ko.observable(info.albumTitle);
    this.artistName  = ko.observable(info.artistName);
    this.totalTime   = ko.observable(info.totalTime);
}

function QueueViewModel(user) {
    this.user = user;
    this.items = ko.observableArray();

    this.count = ko.computed(function() {
        return this.items().length;
    }, this);
}
QueueViewModel.prototype.remove = function(item) {
    rpc("dequeue", [this.user.name(), item.id()], updateJukebox);
    this.items.remove(item);
}
QueueViewModel.prototype.update = function(items, infos) {
    this.items.removeAll();
    for (var i = 0; i < items.length; i++) {
        this.items.push(new QueueItem(items[i], infos[i], this));
    }
}
QueueViewModel.prototype.setup = function() {
    $("#queue").on("click", "li.item", function() {
        var item = ko.dataFor(this);
        item.queue.remove(item);
    });
}
