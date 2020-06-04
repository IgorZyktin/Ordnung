$(document).ready(function () {
    $("div[class^='alert']").on("click", function () {
        kill(this);
    })

    $('#btn_retry').on("click", function () {
        refresh();
        return false;
    });

    $('#btn_restore').on("click", function () {
        relocate('/restore');
        return false;
    });

    $('#btn_register').on("click", function () {
        relocate('/register');
        return false;
    });

    $('#btn_go_main').on("click", function () {
        relocate('/');
        return false;
    });

    $("div[class^='day']").on("click", function () {
        let date = $(this).attr('date');
        relocate('/day?date=' + date);
    })

    $('#menu_toggle').on("click", function () {
        $('#menu').toggle();
    })

});

function refresh() {
    // reload whole page
    document.location.reload();
}

function kill(target) {
    // delete this. used on alerts to close them
    $(target).remove();
}

function relocate(url) {
    // change location
    window.location.href = url;
}
