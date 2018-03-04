$(document).ready(function() {
    $("#form_select_luna").find("option:last").attr("selected","selected");

    var month_selection = document.getElementById("form_select_luna");
    month_selection.addEventListener('change',function() {
       fill_table(month_selection.selectedIndex);
       set_up_columns(month_selection.selectedIndex);
    });

    fill_table(month_selection.selectedIndex);
    set_up_columns(month_selection.selectedIndex);

});

/**
 * Fill up the table
 * @param month selected month
 */
function fill_table(month) {

    month += 1;
     var ajx = $.getJSON("api/money/totals/" + month + "/",function(data,status) {
        if (status === "success") {
           $('#myTable').find('tbody > tr').remove();
           $.each(data, function (index, value) {
               $('#myTable').find('>tbody:last-child').append(
                   '<tr>' +
                       '<td class="align-middle">' + value.categorie+ '</td>' +
                       '<td class="align-middle">' + value.total + '</td>' +
                       '<td class="align-middle">' + value.total_prev_1 + '</td>' +
                       '<td class="align-middle">' + value.total_prev_2 + '</td>' +
                   '</tr>'
               );
            });
        }
    });
}

/**
 * Set up table header
 * @param selected_month is based 0
 */
function set_up_columns(selected_month) {

    //write in the title the month name
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    $('#myTable').find('thead > tr').remove();

    if (selected_month === 0) {
        $('#myTable').find('thead').append(
            '<tr>' +
            '<th>Categorie</th>' +
            '<th>' + monthNames[selected_month] +'</th>' +
            '</tr>'
        );
    }
    else if (selected_month === 1) {
        $('#myTable').find('thead').append(
            '<tr><th>Categorie</th>' +
            '<th>' + monthNames[selected_month] +'</th>' +
            '<th>' + monthNames[selected_month - 1] +'</th></tr>'
        );
    }
    else {
        $('#myTable').find('thead').append(
            '<tr><th>Categorie</th>' +
            '<th>' + monthNames[selected_month] +'</th>' +
            '<th>' + monthNames[selected_month - 1] +'</th>' +
            '<th>' + monthNames[selected_month - 2] +'</th></tr>'
        );
    }
}
