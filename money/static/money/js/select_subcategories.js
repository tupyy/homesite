$(function () {
        $('#date').datepicker({
            'dateFormat' : 'dd/mm/yy'
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

$(document).ready(function() {
   var categorySelect = document.getElementById('category');
   var subcategorySelect = document.getElementById('subcategory');
   categorySelect.addEventListener("change", function() {

       category_name = categorySelect.item(categorySelect.selectedIndex).text;
       $.get("/api/money/subcategory/" + category_name + "/category/",function(data,status) {
           if (status === "success") {

               removeOptions(subcategorySelect);
               for (var j = 0; j < data.subcategories.length; j++) {
                   var dict = data.subcategories[j];
                   var opt = document.createElement('option');
                   opt.innerHTML = dict;
                   subcategorySelect.appendChild(opt);
               }
           }
       });
    });

    document.getElementById('category').options[0].selected='selected';
    document.getElementById('category').onchange();



})();