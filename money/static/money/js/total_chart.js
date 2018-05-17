$(document).ready(function() {
    'use strict';

    document.getElementById('select_categorie').options[0].selected = 'selected';
    $("#select_luna option:last").attr("selected", "selected");

    var month_select = document.getElementById('select_luna');
    month_select.addEventListener("change", function () {
        var month_index = month_select.selectedIndex + 1;
        get_month_totals(month_index);
    });

    // Load the Visualization API and the corechart package.
    google.charts.load('current', {'packages': ['corechart']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(get_month_totals(month_select.selectedIndex + 1));

});

/**
 * Get totals from api call:  /api/money/total/{month}/months_total/"
 */
function get_month_totals(month) {

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/api/money/total/' + month + '/months_total/',
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: 'GET',
        data: {},
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.responseText);
        }
    }).done(function (data) {
        drawMonthTotalChart(JSON.parse(data));
    });
}

/**
 * Draw the line chart for whole year for the selected category
 * @param data
 * @param categorie
 */
function drawMonthTotalChart(data) {

    var chart_array = [];
    var title_array = ['Month', 'Total', 'Venituri'];
    var data_array = [];

    data_array.push(title_array);

    //add data
    for (var key in data) {
        var row = [key];
        row.push(parseFloat(data[key]));
        row.push(parseFloat(4400));

        data_array.push(row);
    }

    var chart_data = google.visualization.arrayToDataTable(data_array);
    var options = {
        title: "Total cheltuieli",
        legend: { position: 'right' },
        vAxis: {
            title: 'Cheltuieli €',
            titleTextStyle: {
                color: 'red'
            }
        },
        hAxis: {
            gridlines: {
                color: '#eee'
            }
        },
        pointSize: 10
    };

    var chart = new google.visualization.LineChart(document.getElementById('total_chart'));

    chart.draw(chart_data, options);

}
