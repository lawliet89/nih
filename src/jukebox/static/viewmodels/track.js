function TrackViewModel() {
    this.trackName = ko.observable("?");
    this.artistName = ko.observable();
    this.albumTitle = ko.observable();
    this.trackNumber = ko.observable();
    this.artCacheHash = ko.observable();

    this.hasArt = ko.computed(function() {
        return this.artCacheHash() != null;
    }, this);
    this.artUrl = ko.computed(function() {
        if (this.hasArt()) {
            return "cache/" + this.artCacheHash() + ".jpeg";
        } else {
            return "static/no-art.png";
        }
    }, this);
}
TrackViewModel.prototype.update = function(metadata) {
    this.trackName(metadata.trackName);
    this.artistName(metadata.artistName);
    this.albumTitle(metadata.albumTitle);
    this.trackNumber(metadata.trackNumber);
    this.artCacheHash(metadata.cacheHash);
}
TrackViewModel.prototype.clear = function() {
    this.trackName("...");
    this.artistName("");
    this.albumTitle("");
    this.trackNumber("");
    this.artCacheHash(null);
}
