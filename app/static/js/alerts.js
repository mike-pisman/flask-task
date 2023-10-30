let alertID = 0;

addAlert = function (message, alertType) {
    // Increment the alert ID
    alertID++;

    // Perpend the new alert to the alert placeholder
    $('#alert_placeholder').prepend('<div id="alert'+ alertID +'" class="alert alert-' + alertType + ' alert-dismissible fade show" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');

    // Remove the alert after 3 seconds
    $('#alert' + alertID).delay(3000).fadeOut(500, function () {
        $(this).remove();
    });
    
    // If the alert list is over 3, remove all alerts after the 3rd one
    var alertList = document.querySelectorAll('.alert')
    if (alertList.length > 3) {
        for (var i = 3; i < alertList.length; i++) {
            $(alertList[i]).dequeue().fadeOut(500, function () {
                $(this).remove();
            });
        }
    }
}