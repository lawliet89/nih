// This class splits up the task of doing a search,
// which may return hundreds of results, into smaller
// chunks in order to gain a more responsive UI.
//
// It does this in two ways. Firstly, it makes three
// requests to the server, each time requesting more
// results: First 10, then 11 - 100, then 101 - 1000.
// This means that the first few results come back 
// more quickly.
//
// Secondly, when we receive the largest result set,
// it adds them to the view model in slices of 100
// so that the UI remains responsive.
//
// Possibly this whole class needs replacing with a
// proper threading-based approach.
function Query(terms, searcher) {
    this.terms = terms;
    this.searcher = searcher;
    this.alive = true;
    this.maxResults = 1000;
}

Query.prototype.start = function() {
    this.search(10, 0);
}
// Stops the ongoing query both from making more
// requests to the server, and from adding any more
// received results to the UI.
Query.prototype.kill = function() {
    this.alive = false;
}
// Fetches 'count' results from the server, starting
// from 'skip'. e.g. Get 11 - 100.
Query.prototype.search = function(count, skip) {
    var me = this;
    rpc("search", [this.terms, count, skip], function(results) {
        me.handleSearchResults(results, function() {
            if (count < me.maxResults && me.alive) {
                // Fetch a larger result set from the server
                me.search(count * 10, count);
            }
        });
    });
}
// Adds the received results to the UI, a chunk
// at a time
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
            setTimeout(handle, 100);
        } else {
            onFinish();
        }
    };
    // Using setTimeout we add the results to the UI
    // a bit a time, repeatedly invoking this handle
    // method
    handle();
}
Query.prototype.equals = function(other) {
    return other != null
        && arraysEqual(this.terms, other.terms);
}

function arraysEqual(a, b) {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length != b.length) return false;

  for (var i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) {
         return false;
      }
  }
  return true;
}
