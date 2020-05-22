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
