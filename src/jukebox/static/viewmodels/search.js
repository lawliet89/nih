function SearchItem(url, info) {
    this.url = ko.observable(url);
    this.metadata = new Metadata(url, info);
    this.folder = this.metadata.folder;
}

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
    this.user = user;

    this.query.extend({ rateLimit: { timeout: 200, method: "notifyWhenChangesStop" } });
    this.query.subscribe(function(newQuery) {
        if (newQuery) {
            tabs.select(".search");
            rpc("search", [newQuery.split(/ +/)], function(results) {
                me.handleSearchResults(results);
            });
        }
    });    
}
SearchViewModel.prototype.handleSearchResults = function(results) {
    var me = this;
    var groupLookup = {};
    var groups = [];

    var getGroup = function(item) {
        var group = groupLookup[item.folder];
        if (!group) {
            group = new ResultsGroup(item.folder);
            groups.push(group);
            groupLookup[item.folder] = group;
        }
        return group;
    }

    results.forEach(function(r) {
        var item = new SearchItem(r.url, r.info);        
        getGroup(item).add(item);
    });
    this.groups(groups);
}
SearchViewModel.prototype.setup = function() {    
    var me = this;
    $("#tabs li.search").click(function() {
        $("#search-box").focus();
        if (me.query()) {
            tabs.select(".search"); 
        }
    });
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
