$(document).ready(function() {
    let month_select = document.getElementById('select_luna');
    month_select.addEventListener("change", function() {
       month_index = month_select.selectedIndex + 1;
       window.location.href='/money/payment/'+ month_index + '/';
    });

});



