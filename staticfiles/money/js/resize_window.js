$(document).ready(function () {
    if ($(window).width() <= 750) {
        // get header
        const header = [];
        $(".total-categories-table thead tr th").each(function () {
            header.push($(this).text());
        });

        let counter = 1;
        $(".total-categories-table tbody tr td").each(function (index) {
            if (index > 0) {
                $(this).attr('data-content',header[counter]);
                counter++;
                 if (counter > header.length) {
                     counter = 1;
                }
            }
        });
    }
});
