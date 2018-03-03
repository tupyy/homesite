$(document).ready(function() {
    document.getElementById('select_categorie').options[0].selected='selected';
    var month_select = document.getElementById('select_luna');
    month_select.addEventListener("change", function() {
        month_index = month_select.selectedIndex + 1;
        window.location.href='/money/payment/view/'+ month_index + '/';
    });
});


function removeOptions(selectbox)
{
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
    {
        selectbox.remove(i);
    }
}

$(function() {
   var categorySelect = document.getElementById('select_categorie');
   var subcategorySelect = document.getElementById('select_subcategorie');
   categorySelect.addEventListener("change", function() {

       category_name = categorySelect.item(categorySelect.selectedIndex).text;
       if (category_name != "") {
           $.get("/api/money/subcategory/" + category_name + "/category/",function(data,status) {
               if (status == "success") {

                   removeOptions(subcategorySelect);
                   for (var j = 0; j < data.subcategories.length; j++) {
                       var dict = data.subcategories[j];
                       var opt = document.createElement('option');
                       opt.innerHTML = dict;
                       subcategorySelect.appendChild(opt);
                   }
               }
            });
       }
       else {
           removeOptions(subcategorySelect);
       }

    });

    //change table
    // var monthSelect = document.getElementById('select_luna');
    //     monthSelect.addEventListener("change", function() {
    //     month_index = this.selectedIndex + 1;
    //     $.getJSON("/api/money/payment?month=" + month_index,function(data,status) {
    //        if (status === "success") {
    //             $('#monthTable').find('tbody > tr').remove();
    //             $.each(data,function(index,value) {
    //                 $('#monthTable').find('>tbody:last-child').append(
    //                     '<tr>' +
    //                     '<td>' + value.user + '</td>' +
    //                     '<td>' + value.category + '</td>' +
    //                     '<td>' + value.subcategory + '</td>' +
    //                     '<td>' + value.date + '</td>' +
    //                     '<td>' + value.sum + '</td>' +
    //                     '<td>' + value.option_pay + '</td>' +
    //                     '<td>' + value.nb_option + '</td>' +
    //                     '<td>' + value.comments + '</td>' +
    //                     '<td class="td-btn">\n' +
    //                     '<div class="div-btn">\n' +
    //                     '<button type="button" class="btn btn-warning">Modificare</button>\n' +
    //                     '<button type="button" class="btn btn-danger">Stergere</button>\n' +
    //                     '</div>\n' +
    //                     '</td>' +
    //                     '<\tr>'
    //                 );
    //             });
    //        }
    //     });
    // });
});

