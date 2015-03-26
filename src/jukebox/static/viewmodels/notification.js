function NotificationViewModel() {
	var self = this;

	this.permission = ko.observable();
	// Just a bunch of ID numbers to track notifications. Not really used now.
	this.id = 0;
	// Number of seconds to show the notification
	this.timeout = 5;

	this.status = ko.observable("");
	this.artistName = ko.observable(null);
	this.trackTitle = ko.observable(null);

	this.notificationState = ko.computed(function() {
		var body = "";
		if (self.artistName() !== null && self.trackTitle() !== null) {
			body = self.artistName() + " – " + self.trackTitle();
		}
		return {
			body: body,
			status: self.status()
		}
	});

	this.notificationState.extend({ rateLimit: 500 });
	this.notificationState.subscribe(function(newValue){
		if (newValue.body !== "" && newValue.status === "playing") {
			self.notify(newValue.body);
		}
	});
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

NotificationViewModel.prototype.update = function(status) {
	if (status.status) {
		this.status(status.status);
	} else {
		this.status("");
	}

    if (status.info) {
    	if (status.info.trackName) {
	        this.trackTitle(status.info.trackName);
	    } else {
	        this.trackTitle(splitPath(status.entry.url).name);
	    }
	    this.artistName(status.info.artistName);
    } else {
    	this.trackTitle(null);
    	this.artistName(null);
    }
}

NotificationViewModel.prototype.notify = function(body) {
	var notification = new Notify("Jukebox", {
	    body: body,
	    tag: this.id,
	    timeout: this.timeout
	});
	notification.show();
	++this.id;
	return notification;
}
