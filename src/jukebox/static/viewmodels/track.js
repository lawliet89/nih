function TrackViewModel() {
    this.trackName = ko.observable("?");
    this.artistName = ko.observable();
    this.albumTitle = ko.observable();
    this.trackNumber = ko.observable();
    this.artCacheHash = ko.observable();
    this.hasTrack = ko.observable(false);

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
TrackViewModel.prototype.update = function(url, metadata) {
    if (metadata.trackName) {
        this.trackName(metadata.trackName);
    } else {
        this.trackName(splitPath(url).name);
    }
    this.artistName(metadata.artistName);
    this.albumTitle(metadata.albumTitle);
    this.trackNumber(metadata.trackNumber);
    this.artCacheHash(metadata.cacheHash);
    this.hasTrack(true);
}
TrackViewModel.prototype.clear = function() {
    this.trackName("Nothing playing");
    this.artistName("");
    this.albumTitle("");
    this.trackNumber("");
    this.artCacheHash(null);
    this.hasTrack(false);
}
