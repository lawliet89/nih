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
}
PlayerViewModel.prototype.update = function(status) {
    if (status.info) {
        this.track.update(status.info);
        this.progress.update(status.elapsedTime, status.info.totalTime);
    } else {
        this.track.clear();
    }
    this.status(status.status);
}
PlayerViewModel.prototype.play = function() {
    rpc("pause", [false, this.user.name()], updatePlayer); 
}
PlayerViewModel.prototype.pause = function() {
    rpc("pause", [true, this.user.name()], updatePlayer);
}
PlayerViewModel.prototype.skip = function() {
    rpc("skip", [this.user.name()], updatePlayer); 
}

function incrementPlayer() {
    var player = jukebox.player;
    if (player.active()) {
        player.progress.increment();
    }
    setTimeout(incrementPlayer, 1000);
}
function updatePlayer(status) {
    jukebox.player.update(status);
}
function updateVolume(status) {
    jukebox.player.volume.update(status);
}
