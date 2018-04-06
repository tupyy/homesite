$(document).ready(function () {
    'use strict';

    document.getElementById('select_categorie').options[0].selected='selected';
    $("#select_luna option:last").attr("selected","selected");

    var month_select = document.getElementById('select_luna');
    month_select.addEventListener("change", function() {
       var month_index = month_select.selectedIndex + 1;
       get_totals(month_index, get_category());
    });

    var categorie_select = document.getElementById("select_categorie");
    categorie_select.addEventListener("change", function() {
       get_totals(get_month(), get_category());
    });


    // Load the Visualization API and the corechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(get_totals(month_select.selectedIndex + 1,get_category()));

});



function drawChart(data, categorie) {

    if ( !isEmpty(data) ) {
        var chart_array = [['Subcategorie', 'Suma']];
        for (var key in data) {
            var entry = [key, parseFloat(data[key])]
            chart_array.push(entry);
        }

        var chart_data = google.visualization.arrayToDataTable(chart_array);
        var options = {
            title: categorie,
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
 * Get totals from api call:  /api/money/category/{month}/total/category={category_name}
 */
function get_totals(month, categorie) {

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/api/money/category/'+month+'/total?category='+categorie,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: 'GET',
        data: {},
        error:function(XMLHttpRequest, textStatus, errorThrown){
           console.log(XMLHttpRequest.responseText);
        }
    }).done(function(data) {
        drawChart(JSON.parse(data),categorie);
    });
}




