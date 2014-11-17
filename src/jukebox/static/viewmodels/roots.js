function Root(url, count) {
    this.url = ko.observable(url);
    this.count = ko.observable(count);
}

function RootsViewModel() {
    this.all = ko.observableArray();
    this.rescans = ko.observableArray();
    this.newRoot = ko.observable();
    this.open = false;

    this.count = ko.computed(function() {
        return this.all().length;
    }, this);
    this.rescan_count = ko.computed(function() {
        return this.rescans().length;
    }, this);
}
RootsViewModel.prototype.update = function(roots) {
    var me = this;
    this.all.removeAll();
    roots.forEach(function(r) {
        me.all.push(new Root(r.url, r.count));
    });
}
RootsViewModel.prototype.updateRescans = function(rescans) {
    this.rescans(rescans);
}
RootsViewModel.prototype.handleRescan = function(result) {
    if (result.result == 'success') {
        rpc("all_roots", [], updateRoots, "config");
    } else {
        alert("Unable to scan " + result.root);
    };
    this.updateRescans(result.current_rescans);
}
RootsViewModel.prototype.setup = function() {
    var me = this;
    // Open the modal dialog
    $("#manage-roots").click(function (event) {
        refreshRoots();
        me.newRoot('http://');
        showModal($("#roots"), function() { me.open = false; });
        me.open = true;
        event.preventDefault();
    });
    // Remove a root
    $("#roots").on("click", ".remove", function(event) {
        var root = ko.dataFor(this);
        rpc('remove_root', [root.url()], updateRoots, 'config');
        event.preventDefault();
    });
    // Rescan a root
    $("#roots").on("click", ".rescan", function(event) {
        var root = ko.dataFor(this);
        rpc('rescan_root', [root.url()], handleRescan, 'config');
        event.preventDefault();
    });
    // Add a new root
    $("#roots form").submit(function(event) {
        rpc('rescan_root', [me.newRoot()], handleRescan, 'config');
        event.preventDefault();
    });   
}
function refreshRoots() {
    rpc("all_roots", [], updateRoots, "config");
    rpc("current_rescans", [], updateRescans, "config");
}
function updateRoots(roots) {
    jukebox.roots.update(roots);
}
function updateRescans(rescans) {
    jukebox.roots.updateRescans(rescans);
}
function handleRescan(result) {
    jukebox.roots.handleRescan(result);
}
