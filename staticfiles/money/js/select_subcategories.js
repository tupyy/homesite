$(function () {
        $('#date').datepicker({
            'dateFormat' : 'dd/mm/yy'
        });
});

function get_current_category() {
    var categorySelect = document.getElementById('category');
    return categorySelect.item(categorySelect.selectedIndex).text;
}

function remove_subcategories()
{
    var subcategorySelect = document.getElementById('subcategory');
    var i;
    for(i = subcategorySelect.options.length - 1 ; i >= 0 ; i--)
    {
        subcategorySelect.remove(i);
    }
}

/**
 * make the call to get the subcategories for a category
 * @param category_name
 */
function add_subcategories(category_name) {
     let subcategorySelect = document.getElementById('subcategory');
     $.get("/api/money/subcategory/" + category_name + "/category/",function(data,status) {
           if (status === "success") {
               for (var j = 0; j < data.subcategories.length; j++) {
                   var dict = data.subcategories[j];
                   var opt = document.createElement('option');
                   opt.value = dict.id;
                   opt.innerHTML = dict.name;
                   subcategorySelect.appendChild(opt);
               }
           }
       });
}

$(document).ready(function() {
   let categorySelect = document.getElementById('category');
   categorySelect.addEventListener("change", function() {
       remove_subcategories();
       add_subcategories(get_current_category());
    });
});