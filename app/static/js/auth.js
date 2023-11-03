signup = function(){ 
    form = $('#form-signup');
    formData = form.serialize();

    $.ajax({
        url: '/signup',
        type: 'POST',
        accepts: 'application/json',
        data: formData,
        success: function (data) {
            window.open("/login", "_self");
        },
        error: function (data) {
            response = JSON.parse(data.responseText);
            console.log(response);
            addAlert(response.error, "danger");
        }
    });
}