var player;
var username = "bob";
function PlayerViewModel(trackName, status) {
    this.trackName = ko.observable(trackName);
    this.status = ko.observable(status);
    this.elapsedTime = ko.observable(0);
    this.totalTime = ko.observable(0.1);
    this.volume = new VolumeViewModel();

    this.progress = ko.computed(function() {
        return ((this.elapsedTime() * 100) / this.totalTime()) + "%";
    }, this);
    this.elapsedTimeText = ko.computed(function() {
        return this.formatTime(this.elapsedTime());
    }, this);
    this.totalTimeText = ko.computed(function() {
        return this.formatTime(this.totalTime());
    }, this);
    this.active = ko.computed(function() {
        return this.status() == 'playing';
    }, this);

    var controls = $("#player .controls");
    controls.find(".play").click(this.play);
    controls.find(".pause").click(this.pause);
    controls.find(".skip").click(this.skip);
}
PlayerViewModel.prototype.update = function(status) {
    if (status.entry) {
        this.trackName(status.info.trackName);
    } else {
        this.trackName("");
    }
    if (status.info) {
        this.totalTime(status.info.totalTime);
    }
    this.status(status.status);
    this.elapsedTime(status.elapsedTime);
}
PlayerViewModel.prototype.play = function() {
    rpc("pause", [false, username], updatePlayer); 
}
PlayerViewModel.prototype.pause = function() {
    rpc("pause", [true, username], updatePlayer);
}
PlayerViewModel.prototype.skip = function() {
    rpc("skip", [username], updatePlayer); 
}
PlayerViewModel.prototype.formatTime = function(seconds) {
    function pad(num) {
        return num < 10 ? "0" + num : num;
    }
    seconds = Math.floor(seconds);
    return (seconds >= 3600 ? pad(Math.floor(seconds / 3600)) + ":" : "")
        + pad(Math.floor(seconds / 60)) + ":"
        + pad(seconds % 60);
}

function incrementPlayer() {
    if (player.active() && player.elapsedTime() < player.totalTime()) {
        player.elapsedTime(player.elapsedTime() + 1);
    }
    setTimeout(incrementPlayer, 1000);
}
function setupPlayer() {
    player = new PlayerViewModel("?", "?");
    ko.applyBindings(player);
    incrementPlayer();
};
function updatePlayer(status) {
    player.update(status);
}
function updateVolume(status) {
    player.volume.update(status);
}
