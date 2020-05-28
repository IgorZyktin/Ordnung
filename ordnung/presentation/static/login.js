$(document).ready(function () {

    $('#btn_login').on("click", function () {
        document.location.reload();
        return false;
    });

    $('#btn_restore').on("click", function () {
        document.location.href = '/restore';
        return false;
    });

    $('#btn_register').on("click", function () {
        document.location.href = '/register';
        return false;
    });
});