$(document).ready(function () {
    let url;

    $('.btn-delete').click(function (e) {
        let $modalDiv = $('#confirm-delete');
        e.preventDefault();
        $modalDiv.modal('show');
        url = $(this).attr('href');
    });


    $('.btn-ok').click(function (event) {
        $.ajax({
            url: url,
            type: 'DELETE',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function () {
                $('#confirm-delete').modal('hide');
                location.reload();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.statusText + ' ' + jqXHR.responseText)
            }
        });

    });
});



