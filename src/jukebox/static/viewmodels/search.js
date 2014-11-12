function SearchItem(url, info) {
    this.url = ko.observable(url);
    this.metadata = new Metadata(url, info);
    this.folder = this.metadata.folder;
}

// For grouping the results by folder
function ResultsGroup(url) {
    var parts = parseUri(url);
    this.items = ko.observableArray();
    this.url = url;
    this.host = parts.authority;
    this.path = parts.directory;
    this.folder = splitPath(parts.directory).name;
    
    this.count = ko.computed(function() {
        return this.items().length;
    }, this);
}
ResultsGroup.prototype.add = function(item) {
    this.items.push(item);
}

function SearchViewModel(user) {
    var me = this;
    this.queryString = ko.observable("");
    this.groups = ko.observableArray();
    this.groupLookup = {};
    this.user = user;
    this.currentQuery = null;

    this.count = ko.computed(function() {
        var number = 0;
        this.groups().forEach(function(g) { number += g.count(); });
        return number;
    }, this);

    this.searchTerms = ko.computed(function() {
        return this.queryString()
            .split(/ +/)
            .filter(function(t) { return t != ""; });
    }, this);
    this.searchTerms.extend({ rateLimit: { timeout: 400, method: "notifyWhenChangesStop" } });
    this.searchTerms.subscribe(function(terms) {
        if (terms.length) {
            tabs.select(".search");
            me.setQuery(new Query(terms, me));            
        }
    });    
}
SearchViewModel.prototype.setQuery = function(newQuery) {
    if (!newQuery.equals(this.currentQuery)) {
        this.clear();
        if (this.currentQuery) {
            this.currentQuery.kill();
        }
        this.currentQuery = newQuery;
        newQuery.start();
    }
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
        if (me.queryString()) {
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
