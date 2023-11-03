signup = function(){
    form = $('#form-signup');
    formData = {
        email: $('#email').val(),
        name: $('#name').val(),
        password: $('#password').val()
    }

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
            addAlert(response.error, "danger");
        }
    });
}

login = function(){ 
    form = $('#form-login');
    formData = form.serialize();

    formData = {
        email: $('#email').val(),
        password: $('#password').val(),
        remember: $('#remember-me').is(':checked')
    }

    console.log(formData);

    $.ajax({
        url: '/login',
        type: 'POST',
        accepts: 'application/json',
        data: formData,
        success: function (data) {
            window.open("/", "_self");
        },
        error: function (data) {
            response = JSON.parse(data.responseText);
            addAlert(response.error, "danger");
        }
    });
}

$(document).ready(function() {
    $('#form-login').submit(function(e){
        e.preventDefault();
        login();
    });

    $('#form-signup').submit(function(e){
        e.preventDefault();
        signup();
    });
});