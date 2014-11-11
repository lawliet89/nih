function Query(queryString, searcher) {
    this.q = queryString.split(/ +/);
    this.searcher = searcher;
    this.alive = true;
    this.maxResults = 1000;
    this.search(10, 0);
}
Query.prototype.kill = function() {
    this.alive = false;
}
Query.prototype.search = function(count, skip) {
    var me = this;
    rpc("search", [this.q, count, skip], function(results) {
        me.handleSearchResults(results, function() {
            if (count < me.maxResults && me.alive) {
                me.search(count * 10, count);
            }
        });
    });
}
Query.prototype.handleSearchResults = function(results, onFinish) {
    var me = this;
    var i = 0;
    var step = 100;
    var handle = function() {
        if (i < results.length && me.alive) {
            var target = Math.min(results.length, i + step);
            while (i < target) {
                var r = results[i];
                var item = new SearchItem(r.url, r.info);        
                me.searcher.getGroup(item).add(item);
                i++;
            }
            setTimeout(handle, 10);
        } else {
            onFinish();
        }
    };
    handle();
}
