function NotificationViewModel() {
	this.permission = ko.observable();
	this.updatePermission();
}

NotificationViewModel.prototype.setup = function() {
	// Try to ask for permission on page load
	this.getPermission(this);
}

// Needs to function as a KO click handler as well
NotificationViewModel.prototype.getPermission = function(self) {
	if (self.permission() === "default") {
		Notify.requestPermission(self.updatePermission,
			self.updatePermission);
	}
}

NotificationViewModel.prototype.updatePermission = function() {
	// Possible values are: default, granted, denied, or null (if unsupported)
	this.permission(Notify.permissionLevel);
}
