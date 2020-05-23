$(document).ready(function () {
    $( "div[class^='day']" ).on("click", function () {
        let date = $(this).attr('date');
        relocate_with_args('/day?date=' + date);
    })
    $('#menu_toggle').on("click", function () {
        $('#menu').toggle();
    })
});

