function VolumeViewModel() {
    this.volume = ko.observable(0);
    this.who = ko.observable("");
    this.direction = ko.observable("");

    this.volume.subscribe(function(newVolume) {
        rpc("set_volume", [username, newVolume]);
    });
}
VolumeViewModel.prototype.update = function(status) {
    this.volume(status.volume);
    this.who(status.who);
    this.direction(status.direction);
}
