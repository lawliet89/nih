function VolumeViewModel(user) {
    this.volume = ko.observable(null);
    this.who = ko.observable("");
    this.direction = ko.observable("");

    this.volume.extend({ rateLimit: 1000 });
    this.volume.subscribe(function(newVolume) {
        var value = parseInt(newVolume);
        if (!isNaN(value)) {
            rpc("set_volume", [user.name(), value], updateVolume);
        }
    });
    this.volumeChanged = ko.computed(function() {
        return this.who() && this.direction();
    }, this);
}
VolumeViewModel.prototype.update = function(status) {
    this.volume(status.volume);
    this.who(status.who);
    this.direction(status.direction);
}
