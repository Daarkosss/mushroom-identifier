$(document).ready(function(){
    $('#upload-form').on('submit', function(event){
        event.preventDefault();
        var formData = new FormData(this);
        $('#loading').addClass('active')
        $.ajax({
            url: '/upload',
            data: formData,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $('#loading').removeClass('active')
                if (response.redirect) {
                    window.location.href = response.redirect;
                }
            },
            error: function(response){
                $('#loading').removeClass('active')
                if (response.responseJSON.error) {
                    alert(response.responseJSON.error);
                }
            }
        });
    });

    $('#login-form').on('submit', function(event){
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            url: '/login',
            data: formData,
            type: 'POST',
            success: function(response){
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else if (response.error) {
                    alert(response.error);
                }
            },
            error: function(response){
                if (response.responseJSON.error) {
                    alert(response.responseJSON.error);
                } else {
                    alert("Unexpected login error");
                }
            }
        });
    });

    $('#register-form').on('submit', function(event){
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            url: '/register',
            data: formData,
            type: 'POST',
            success: function(response){
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else if (response.error) {
                    alert(response.error);
                }
            },
            error: function(response){
                if (response.responseJSON.error) {
                    alert(response.responseJSON.error);
                } else {
                    alert("Unexpected register error");
                }
            }
        });
    });

    $('#file-input').on('change', function() {
        var fileName = $(this).val().split('\\').pop();
        $('#file-name').text(fileName);
    });
});