$(document).ready(function() {
    document.getElementById('select_categorie').options[0].selected='selected';

    var month_select = document.getElementById('select_luna');
    month_select.addEventListener("change", function() {
       month_index = month_select.selectedIndex + 1;
       window.location.href='/money/payment/view/'+ month_index + '/';
    });

    var delete_button = document.getElementById('delete_button');
    attach_delete_event(delete_button);
});

/**
 * Attach on click event
 * @param button
 */
function attach_delete_event(button) {
    button.addEventListener("click",function() {
       delete_payment(button.getAttribute("payment_id"));
    });
}
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
                    '<td class="td-comments">' + value.comments + '</td>' +
                    '<td class="td-btn">\n' +
                    '<div class="div-btn">\n' +
                    '<button type="button" class="btn btn-warning btn-sm" id="modify_button">Modificare</button>\n' +
                    '<button type="button" class="btn btn-danger btn-sm" id="delete_button" payment_id="'+ value.id +'">Stergere</button>\n' +
                    '</div>\n' +
                    '</td>' +
                    '<\tr>'
                );
                var delete_button = document.getElementById('delete_button');
                attach_delete_event(delete_button);
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

function csrfSafeMethod(method) {
   return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Delete a payment
 * Make a DELETE call to /money/payment/{id}/
 * @param id
 */
function delete_payment(id) {

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/api/money/payment/' + id + '/',
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: 'DELETE',
        data: {},
        error:function(XMLHttpRequest, textStatus, errorThrown){
           console.log(XMLHttpRequest.responseText);
        }
    }).done(function() {

        if ( !get_category() ) {
            filter_payments("","",get_month());
        }
        else {
            filter_payments(get_category(),get_subcategory(),get_month());
        }

    });
}
/**
 * Append subcategories when category changes
 */
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

