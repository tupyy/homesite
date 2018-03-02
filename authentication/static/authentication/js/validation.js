(function() {
    "use strict";

    $("#password_input").change(function() {
        var pass =  $("#password_input").val();
        if (pass.length < 8) {
            $(this).addClass("is-invalid");
        }
        else {
            $(this).removeClass('is-invalid');
        }
    });

    $("#confirm_password").on('input',function() {
        var pass =  $("#password_input").val();
        var confirm_pass = $("#confirm_password").val();
        if (confirm_pass.length > 8) {
            if (pass != confirm_pass) {
                $(this).addClass("is-invalid");
            }
            else {
                $(this).removeClass('is-invalid');
                $("#submitButton").removeAttr('disabled');
            }
        }

    });
})();