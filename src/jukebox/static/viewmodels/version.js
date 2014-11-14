function VersionViewModel() {
    this.repo = ko.observable();
    this.hash = ko.observable();
    this.timestamp = ko.observable();
    this.url = ko.observable();

    this.when = ko.computed(function() {
        return moment(this.timestamp()).fromNow();
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
}
