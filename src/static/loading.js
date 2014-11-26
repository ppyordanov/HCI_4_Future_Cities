//used before main content is loaded to prompt the user

function loading_animation() {

    $('#loading').hide()
        .ajaxStart(function () {
            $(this).show();
        })
        .ajaxStop(function () {
            $(this).hide();
        });

}
