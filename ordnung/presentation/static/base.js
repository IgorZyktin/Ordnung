$(document).ready(function () {
    $("div[class^='alert']").on("click", function () {
        kill(this);
    })
});

function kill(target) {
    // delete this. used on alerts to close them
    $(target).remove();
}

function relocate(url) {
    // change location
    window.location.href = url;
}
