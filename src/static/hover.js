/**
 * Created by Peter Yordanov on 25.11.2014 г..
 */
$(document).ready(function(){

    //$("[rel='tooltip']").tooltip();

    $('.thumbnail').hover(
        function(){
            $(this).find('.caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.caption').slideUp(250); //.fadeOut(205)
        }
    );

});