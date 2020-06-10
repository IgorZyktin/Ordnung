$(document).ready(function () {
    $('#has_metric').change(function () {
        $("#metrics").toggle();
        $("#metric_name").prop("disabled", !this.checked);
        $("#metric_objective").prop("disabled", !this.checked);
        $("#metric_step").prop("disabled", !this.checked);
    });
});
