$(document).ready(function () {
    $('#menu_toggle').on("click", function () {
        $('#menu').toggle();
    })
});

function relocate_with_args(url) {
    let new_params = '';

    if (!window.location.href.includes('?')) new_params += '?';

    if ($('#menu').css("display") === 'none') new_params += '&menu=0'
    else new_params += '&menu=1'

    window.location.href = url + new_params;
}