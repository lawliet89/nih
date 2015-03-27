function PlayerViewModel(user) {
    var me = this;
    this.status = ko.observable("?");
    this.volume = new VolumeViewModel(user);
    this.progress = new ProgressViewModel();
    this.user = user;
    this.track = new TrackViewModel();

    this.active = ko.computed(function() {
        return this.status() == 'playing';
    }, this);

    var controls = $("#player .controls");
    controls.find(".play").click(function() { me.play(); });
    controls.find(".pause").click(function() { me.pause(); });
    controls.find(".skip").click(function() { me.skip(); });
}
PlayerViewModel.prototype.setup = function() {
    incrementPlayer();
    this.volume.setup();
}
PlayerViewModel.prototype.update = function(status) {
    if (status.info) {
        this.track.update(status.entry.url, status.info, status.entry.username);
        this.progress.update(status.elapsedTime, status.info.totalTime);
    } else {
        this.track.clear();
        this.progress.clear();
    }
    this.status(status.status);
}
PlayerViewModel.prototype.play = function() {
    rpc("pause", [false, this.user.name()], updateJukebox);
}
PlayerViewModel.prototype.pause = function() {
    rpc("pause", [true, this.user.name()], updateJukebox);
}
PlayerViewModel.prototype.skip = function() {
    rpc("skip", [this.user.name()], updateJukebox);
}

function incrementPlayer() {
    var player = jukebox.player;
    if (player.active()) {
        player.progress.increment();
    }
    setTimeout(incrementPlayer, 1000);
}
function updateVolume(status) {
    jukebox.player.volume.update(status);
}
