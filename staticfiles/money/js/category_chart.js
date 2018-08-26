$(document).ready(function () {
    'use strict';

    document.getElementById('select_categorie').options[0].selected = 'selected';
    $("#select_luna option:last").attr("selected", "selected");

    var month_select = document.getElementById('select_luna');
    month_select.addEventListener("change", function () {
        var month_index = month_select.selectedIndex + 1;
        get_totals(month_index, get_category());
    });

    var categorie_select = document.getElementById("select_categorie");
    categorie_select.addEventListener("change", function () {
        get_totals(get_month(), get_category());
        get_year_totals(get_category());
    });


    // Load the Visualization API and the corechart package.
    google.charts.load('current', {'packages': ['corechart']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawCharts(month_select.selectedIndex + 1, get_category()));

});

function drawCharts(month, categorie) {
    get_totals(month, categorie);
    get_year_totals(categorie);
}

/**
 * Draw the pie chart for the selected month and category
 * @param data
 * @param categorie
 */
function drawChart(data, categorie) {

    if (!isEmpty(data)) {
        var chart_array = [['Subcategorie', 'Suma']];
        for (var key in data) {
            var entry = [key, parseFloat(data[key])];
            chart_array.push(entry);
        }

        var chart_data = google.visualization.arrayToDataTable(chart_array);
        var options = {
            title: "Cheltuieli lunare " + categorie,
            is3D: true
        };

        var formatter = new google.visualization.NumberFormat({prefix: '€ '});
        formatter.format(chart_data, 1);
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(chart_data, options);
    }
    else {
        document.getElementById('piechart').innerHTML = "";
        document.getElementById('piechart').innerHTML = "<h5>No data</h5>";
    }
}

/**
 * Draw the line chart for whole year for the selected category
 * @param data
 * @param categorie
 */
function drawYearChart(data, category) {

    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December", "revenues"
    ];
    var chart_array = [];
    var title_array = ['Luna'];

    var subcategories = data['subcategories'];
    for (var i = 0; i < subcategories.length; i++) {
        title_array.push(subcategories[i])
    }

    delete(data['subcategories']);
    chart_array.push(title_array);

    //add data
    for (var month in monthNames) {
        if (monthNames[month] in data) {
             var month_list = [];
            month_list.push(monthNames[month]);
            for (var j = 0; j < data[monthNames[month]].length; j++) {
                month_list.push(parseFloat(data[monthNames[month]][j]));
            }
            chart_array.push(month_list);
        }
    }

    var chart_data = google.visualization.arrayToDataTable(chart_array);
    var options = {
        title: "Cheltuieli anuale - " + category,
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

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(chart_data, options);

}


/**
 * Get totals from api call:  /api/money/category/{month}/total/category={category_name}
 */
function get_totals(month, categorie) {

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/api/money/category/' + month + '/total?category=' + categorie,
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
        drawChart(JSON.parse(data), categorie);
    });
}

/**
 * Get totals from api call:  /api/money/category/{categorie}/year_total/
 */
function get_year_totals(categorie) {

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/api/money/category/' + categorie + '/year_total/',
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
        drawYearChart(JSON.parse(data), categorie);
    });
}





