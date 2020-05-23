function self_delete(button) {
    $(button).remove();
}

// function view_record(record_id) {
//     relocate('/show_record/' + chosen_date + '/' + record_id);
// }
//
// function relocate_month() {
//     relocate('/show_month/' + chosen_date);
// }
//
// function relocate_day() {
//     relocate('/show_day/' + chosen_date);
// }
//
// function relocate_add() {
//     relocate('/add_record/' + chosen_date);
// }

function relocate(url) {
    window.location.href = url;
}

function relocate_with_args(url) {
    let new_params = '';

    if (!window.location.href.includes('?')) new_params += '?';

    let menu = $('#menu');
    if (menu.css("display") !== undefined) {
        if (menu.css("display") !== 'none') new_params += '&menu=1'
        else new_params += '&menu=0'
    }
    window.location.href = url + new_params;
}