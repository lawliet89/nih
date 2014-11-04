function JukeboxViewModel() {
    this.user = new UserViewModel();
    this.player = new PlayerViewModel(this.user);
}
JukeboxViewModel.prototype.setup = function() {
    ko.applyBindings(this);
    this.player.setup();
    this.user.setup();
}
