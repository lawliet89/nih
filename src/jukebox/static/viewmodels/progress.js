function ProgressViewModel() {    
    this.elapsedTime = ko.observable(0);
    this.totalTime = ko.observable(0.1);    

    this.progress = ko.computed(function() {
        return ((this.elapsedTime() * 100) / this.totalTime()) + "%";
    }, this);
    this.elapsedTimeText = ko.computed(function() {
        return this.formatTime(this.elapsedTime());
    }, this);
    this.totalTimeText = ko.computed(function() {
        return this.formatTime(this.totalTime());
    }, this);
}
ProgressViewModel.prototype.formatTime = function(seconds) {
    function pad(num) {
        return num < 10 ? "0" + num : num;
    }
    seconds = Math.floor(seconds);
    return (seconds >= 3600 ? pad(Math.floor(seconds / 3600)) + ":" : "")
        + pad(Math.floor(seconds / 60)) + ":"
        + pad(seconds % 60);
}
ProgressViewModel.prototype.update = function(elapsed, total) {
    this.elapsedTime(elapsed);
    this.totalTime(total);
}
ProgressViewModel.prototype.clear = function() {
    this.elapsedTime(0);
    this.totalTime(0.1);
}
ProgressViewModel.prototype.increment = function() {
    if (this.elapsedTime() < this.totalTime()) {
        this.elapsedTime(this.elapsedTime() + 1);
    }
}
