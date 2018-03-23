$(document).ready(function () {
    $("#form_select_luna").find("option:last").attr("selected", "selected");

    var month_selection = document.getElementById("form_select_luna");
    month_selection.addEventListener('change', function () {
        refresh_table();
    });

    refresh_table();

});


function refresh_table() {
    var month_selection = document.getElementById("form_select_luna");
    var selected_month = month_selection.selectedIndex;

    try {
        erase_table();

        for (var i = 0; i < 3; i++) {
            var month_name = get_month_name(selected_month - i);
            get_data(selected_month - i, function (month, data) {
                fill_table(get_month_name(month), data);
            });
        }
    }
    catch (error) {
        if (error instanceof RangeError) {
            return
        }
        else {
            console.log(error);
        }

    }
}

/**
 * Return the month name
 * @param month integer
 * @return {string}
 */
function get_month_name(month) {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    if (typeof(monthNames[month]) !== "undefined") {
        return monthNames[month];
    }
    else {
        throw new RangeError("Month not found");
    }
}

/**
 * get the total from server
 * @param month
 * @return JSON with totals by category
 */
function get_data(month, callback) {

    //month index starts at 1
    month += 1;

    $.ajax({
        url: "api/money/total/" + month + "/",
        type: 'GET',
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.responseText);
        }
    }).done(function (data) {
        return callback(month - 1, JSON.parse(data));
    });
}

/**
 * Set up table header
 * @param selected_month is based 0
 */
function fill_table(column_name, data) {

    $('#myTable th:last').after('<th>' + column_name + '</th>');
    var rowCount = $('#myTable tr').length;

    if (rowCount === 1) {
        $("#myTable > thead > tr").append("<th>Categorie</th>");
        $('#myTable th:last').after('<th>' + column_name + '</th>');
        $.each(data, function (index, value) {
            $("#myTable > tbody").append("<tr><td>" + index + "</td><td>" + value + "</td></tr>")
    });
    }
    else {
        $.each(data,function(key,value) {
            var tableRow = $('#myTable tr').filter(function() {
               return $(this).text().indexOf(key) >= 0;
            }).closest('tr');
            tableRow.append("<td>" + value + "</td>");
        })
    }


}


function erase_table() {

    $('#myTable').find('thead > tr > th').remove();
    $('#myTable').find('tbody > tr').remove();

}
