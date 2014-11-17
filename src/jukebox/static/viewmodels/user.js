function UserViewModel() {
    this.name = ko.observable("Unknown");
    this.newName = ko.observable();

    var me = this;
    this.name.subscribe(function(newName) {
        me.newName(newName);
        rpc("set_username", [newName]);
    });
}
UserViewModel.prototype.setup = function() {
    var me = this;
    $("#username .name").click(function(e) {
        var modal = $("#edit-username");
        showModal(modal);
        modal.find("input").focus().select();
        e.preventDefault();
    });
    $("#edit-username form").submit(function(e) {
        me.name(me.newName());
        e.preventDefault();
    });
    rpc("get_username", [], function(newName) {
        me.name(newName);
    });
}
