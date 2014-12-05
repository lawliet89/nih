function VolumeViewModel(user) {
    this.volume = ko.observable(null);
    this.who = ko.observable("");
    this.direction = ko.observable("");
    this.user = user;
    this.lastSent = 0;
    this.delay = 1000; // Don't RPC to change volume more than once a second

    this.volume.extend({ rateLimit: 1000 });
    this.volumeChanged = ko.computed(function() {
        return this.who() && this.direction();
    }, this);
}
VolumeViewModel.prototype.setup = function() {
    var me = this;
    $(".volume #volume-control").bind('input', function() {
        if (me.elapsed() > me.delay) {
            var value = parseInt($(this).val());
            if (!isNaN(value)) {
                me.lastSent = new Date().getTime();
                rpc("set_volume", [me.user.name(), value], updateVolume);
            }
        }
    });
}
VolumeViewModel.prototype.update = function(status) {
    this.volume(status.volume);
    this.who(status.who);
    this.direction(status.direction);
}
// Number of millisecond since we last made an RPC
VolumeViewModel.prototype.elapsed = function() {
    return new Date().getTime() - this.lastSent;
}
