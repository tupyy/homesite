$(function () {
    var month_selection = document.getElementById("form_select_luna");
    month_selection.addEventListener('change',function() {

        selected_month = month_selection.selectedIndex + 1;
        var ajx = $.getJSON("api/money/totals/" + selected_month + "/",function(data,status) {
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

        //write in the title the month name
        var monthNames = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];

        $('#myTable').find('thead > tr').remove();

        if (month_selection.selectedIndex == 0) {
            $('#myTable').find('thead').append(
                '<tr>' +
                '<th>Categorie</th>' +
                '<th>' + monthNames[month_selection.selectedIndex] +'</th>' +
                '</tr>'
            );
        }
        else if (month_selection.selectedIndex == 1) {
            $('#myTable').find('thead').append(
                '<tr><th>Categorie</th>' +
                '<th>' + monthNames[month_selection.selectedIndex] +'</th>' +
                '<th>' + monthNames[month_selection.selectedIndex - 1] +'</th></tr>'
            );
        }
        else {
            $('#myTable').find('thead').append(
                '<tr><th>Categorie</th>' +
                '<th>' + monthNames[month_selection.selectedIndex] +'</th>' +
                '<th>' + monthNames[month_selection.selectedIndex - 1] +'</th>' +
                '<th>' + monthNames[month_selection.selectedIndex - 2] +'</th></tr>'
            );
        }
    });

    $(document).ready(function() {
        $("#form_select_luna").find("option:last").attr("selected","selected");
        $("#form_select_luna").trigger('change');
    });

})();


