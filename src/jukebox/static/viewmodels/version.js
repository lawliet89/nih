function VersionViewModel() {
    this.repo = ko.observable();
    this.hash = ko.observable();
    this.timestamp = ko.observable();
    this.url = ko.observable();
    this.now = ko.observable(new Date());

    this.when = ko.computed(function() {
        return moment(this.timestamp()).from(this.now());
    }, this);
}
VersionViewModel.prototype.setup = function() {
    var me = this;
    rpc('get_version', [], function(v) { me.updateVersion(v); });
}
VersionViewModel.prototype.updateVersion = function(version) {
    this.repo(version.repo);
    this.hash(version.hash);
    this.timestamp(version.timestamp);
    this.url(version.url);
    // Every minute, rerender the timestamp
    var me = this;
    setInterval(function() { me.now(new Date()); }, 60 * 1000);
}
