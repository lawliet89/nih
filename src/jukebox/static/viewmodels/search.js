function SearchItem(url, info) {
    this.url = ko.observable(url);
    this.metadata = new Metadata(url, info);
    this.folder = this.metadata.folder;
}

// For grouping the results by folder
function ResultsGroup(url) {
    var parts = parseUri(url);
    var folderParts = splitPath(parts.directory);

    this.items = ko.observableArray();
    this.url = url;
    this.host = parts.authority;
    this.path = folderParts.path;      
    this.folder = folderParts.name;
    
    this.count = ko.computed(function() {
        return this.items().length;
    }, this);
}
ResultsGroup.prototype.add = function(item) {
    this.items.push(item);
}

function SearchViewModel(user) {
    var me = this;
    this.query = ko.observable();
    this.groups = ko.observableArray();
    this.groupLookup = {};
    this.user = user;
    this.currentQuery = null;

    this.count = ko.computed(function() {
        var number = 0;
        this.groups().forEach(function(g) { number += g.count(); });
        return number;
    }, this);

    this.query.extend({ rateLimit: { timeout: 400, method: "notifyWhenChangesStop" } });
    this.query.subscribe(function(q) {
        if (q) {
            tabs.select(".search");
            me.clear();
            if (me.currentQuery) {
                me.currentQuery.kill();
            }
            me.currentQuery = new Query(q, me);
        }
    });    
}
SearchViewModel.prototype.clear = function() {
    this.groupLookup = {};
    this.groups.removeAll();
}
SearchViewModel.prototype.getGroup = function(item) {
    var group = this.groupLookup[item.folder];
    if (!group) {
        group = new ResultsGroup(item.folder);
        this.groups.push(group);
        this.groupLookup[item.folder] = group;
    }
    return group;
}
SearchViewModel.prototype.setup = function() {    
    var me = this;
    $("#tabs li.search").click(function() {
        $("#search-box").focus();
        if (me.query()) {
            tabs.select(".search"); 
        }
    });
    // Enqueue tracks when you click on them in the search results
    $("#search-results").on("click", "li.item", function(event) {
        var li = this;

        $(li).addClass("selected");
        setTimeout(function() { $(li).removeClass("selected") }, 10);

        var item = ko.dataFor(li);
        var tracks = [{ url: item.url()}];
        rpc("enqueue", [me.user.name(), tracks, false], updateJukebox);

        event.preventDefault();        
    });
}
