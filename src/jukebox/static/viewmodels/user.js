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
        var closeModal = showModal(modal);
        modal.find("input").focus().select();
        modal.find("button").click(closeModal);
        e.preventDefault();
    });
    $("#edit-username button.save").click(function() {
        me.name(me.newName());
    });
    rpc("get_username", [], function(newName) {
        me.name(newName);
    });
}
