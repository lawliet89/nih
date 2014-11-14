function Metadata(url, info) {
    this.trackName   = ko.observable();
    this.trackNumber = ko.observable();
    this.albumTitle  = ko.observable();
    this.artistName  = ko.observable();
    this.totalTime   = ko.observable();

    var parts = splitPath(url);
    this.filename = parts.name;
    this.folder = parts.path;
    
    if (info && info.trackName) {
        this.trackName(info.trackName);
        this.trackNumber(info.trackNumber);
        this.albumTitle(info.albumTitle);
        this.artistName(info.artistName);
        this.totalTime(info.totalTime);
    } else {
        this.trackName(this.filename);
    }
}
function splitPath(url) {
    url = unescape(url).replace(/_/g, ' ');
    var index = url.lastIndexOf('/');
    return { 
        path: url.substr(0, index),
        name: url.substring(index + 1),
    };
}
