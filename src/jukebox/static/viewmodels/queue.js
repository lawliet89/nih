function QueueItem(item, info) {
    this.id  = ko.observable(item.id);
    this.who = ko.observable(item.username);
    this.url = ko.observable(item.url);

    this.trackName   = ko.observable(info.trackName);
    this.trackNumber = ko.observable(info.trackNumber);
    this.albumTitle  = ko.observable(info.albumTitle);
    this.artistName  = ko.observable(info.artistName);
    this.totalTime   = ko.observable(info.totalTime);
}

function QueueViewModel() {
    this.items = ko.observableArray();
    this.count = ko.computed(function() {
        return this.items().length;
    }, this);
}
QueueViewModel.prototype.update = function(items, infos) {
    this.items.removeAll();
    for (var i = 0; i < items.length; i++) {
        this.items.push(new QueueItem(items[i], infos[i]));
    }
}
