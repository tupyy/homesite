/*
    get the category
 */
function get_category() {
    var categorySelect = document.getElementById('select_categorie');
    return categorySelect.item(categorySelect.selectedIndex).text;
}

function get_month() {
    var monthSelect = document.getElementById("select_luna");
    return monthSelect.selectedIndex + 1;
}
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
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