$(document).ready(function() {
    document.getElementById('select_categorie').options[0].selected='selected';
    var month_select = document.getElementById('select_luna');
    month_select.addEventListener("change", function() {
        month_index = month_select.selectedIndex + 1;
        window.location.href='/money/payment/view/'+ month_index + '/';
    });
});

/*

 */
function remove_subcategories(selectbox)
{
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
    {
        selectbox.remove(i);
    }
}

/*
 Call api to filter the payments
 */
function filter_payments(category,subcategory,month) {

    url = "";
    if (category && subcategory && month) {
        url = "/api/money/payment?category=" + category + "&subcategory=" + subcategory + "&month=" + month;
    }
    else if ( !category && !subcategory && month) {
        url = "/api/money/payment?month=" + month;
    }

    $.getJSON(url, function (data, status) {
        if (status === "success") {
            $('#monthTable').find('tbody > tr').remove();
            $.each(data, function (index, value) {
                $('#monthTable').find('>tbody:last-child').append(
                    '<tr>' +
                    '<td>' + value.user + '</td>' +
                    '<td>' + value.category + '</td>' +
                    '<td>' + value.subcategory + '</td>' +
                    '<td>' + value.date + '</td>' +
                    '<td>' + value.sum + '</td>' +
                    '<td>' + value.option_pay + '</td>' +
                    '<td>' + value.nb_option + '</td>' +
                    '<td>' + value.comments + '</td>' +
                    '<td class="td-btn">'+
                        '<div class="div-btn">'+
                            '<button type="button" class="btn btn-warning">Modificare</button>' +
                            '<form method="POST" action="{% url "delete_payment" id=payment.id %}">' +
                                '{% csrf_token %}' +
                                '<input type="hidden" name="next_url" value="{{request.path}}"/>' +
                                '<button type="submit" class="btn btn-danger ">Sterge</button>' +
                            '</form>' +
                        '</div>' +
                    '</td>'+
                    '<\tr>'
                );
            });
            $('#monthTable').focus();
        }
    });
}

/*
    Get the subcategory
 */
function get_subcategory() {
    var subcategorySelect = document.getElementById('select_subcategorie');
    return subcategorySelect.item(subcategorySelect.selectedIndex).text;
}

/*
    get the category
 */
function get_category() {
    var categorySelect = document.getElementById('select_categorie');
    return categorySelect.item(categorySelect.selectedIndex).text;
}

/*
    get the month
 */
function get_month() {
    var month_select = document.getElementById('select_luna');
    return month_select.selectedIndex + 1;
}

$(function() {
   var categorySelect = document.getElementById('select_categorie');
   var subcategorySelect = document.getElementById('select_subcategorie');
   categorySelect.addEventListener("change", function() {

       category_name = categorySelect.item(categorySelect.selectedIndex).text;
       if (category_name !== "") {
           $.get("/api/money/subcategory/" + category_name + "/category/",function(data,status) {
               if (status === "success") {

                   remove_subcategories(subcategorySelect);
                   for (var j = 0; j < data.subcategories.length; j++) {
                       var dict = data.subcategories[j];
                       var opt = document.createElement('option');
                       opt.innerHTML = dict;
                       subcategorySelect.appendChild(opt);
                   }
                   filter_payments(get_category(),get_subcategory(),get_month())
               }
            });
       }
       else {
           remove_subcategories(subcategorySelect);
           filter_payments("","",get_month());
       }

    });

    //change table
    var subcategory_select = document.getElementById('select_subcategorie');
    subcategory_select.addEventListener("change", function() {
        filter_payments(get_category(),get_subcategory(),get_month())
    });
});

