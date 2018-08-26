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
            get_data("api/money/total/" + String(selected_month - i + 1) + "/", selected_month - i, function (month, data) {
                fill_table(get_month_name(month), data);
            });

            get_data("/api/money/total/" + + String(selected_month - i + 1) + "/month_total/",selected_month - i, function (month, data) {
                add_foot_data(data);
            });
        }
    }
    catch (error) {
        if (error instanceof RangeError) {
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
function get_data(my_url, month, callback) {

    $.ajax({
        url: my_url,
        async: false,
        type: 'GET',
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.responseText);
        }
    }).done(function (data) {
        return callback(month, JSON.parse(data));
    });
}

/**
 * Set up table header
 * @param selected_month is based 0
 */
function fill_table(column_name, data) {

     var rowCount = $('#myTable tr').length ;

    if (rowCount === 1) {
        $("#myTable > thead > tr").append("<th>Categorie</th>");
        $('#myTable th:last').after('<th>' + column_name + '</th>');

        for (var key in data) {
            $("#myTable > tbody").append("<tr><td>" + key + "</td><td>" + data[key] + "</td></tr>")
        }
    }
    else {

        var current_index = -1;
        $('#myTable tr:first th').each(function () {
            if (comp_month(column_name, $(this).text())) {
               current_index = $(this).index();
            }
        });

        if (current_index === -1) {
            $('#myTable th:last').after('<th>' + column_name + '</th>');
        }
        else {
            $('#myTable').find('th').eq(current_index).after('<th>' + column_name + '</th>');
        }

        $.each(data, function (key, value) {
            var tableRow = $('#myTable tr').filter(function () {
                return $(this).text().indexOf(key) >= 0;
            }).closest('tr');

            if (current_index === -1) {
                tableRow.append("<td>" + value + "</td>");
            }
            else {
                tableRow.find('td').eq(current_index).after("<td>" + value + "</td>");
            }

        })
    }
}

function add_foot_data(data) {

        var current_index = -1;
        $('#myTable tr:first th').each(function () {
            if (comp_month(Object.keys(data)[0], $(this).text())) {
               current_index = $(this).index();
            }
        });

        if (current_index === -1) {
            $('#myTable > tfoot').append('<th>' + data[0] + '</th>');
        }
         $('#myTable > tfoot').find('th').eq(current_index).after('<th>' + data[0] + '</th>');
}

function comp_month(month1, month2) {
    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    var index1 = monthNames.indexOf(month1);
    var index2 = monthNames.indexOf(month2);

    return index1 > index2;
}

function erase_table() {

    $('#myTable').find('thead > tr > th').remove();
    $('#myTable').find('tbody > tr').remove();

}
