

$( document ).ready(function() {
        $('.smallThumbnail').hover(
        function(){
            $(this).find('.smallCaption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.smallCaption').slideUp(250); //.fadeOut(205)
        });


                $('.thumbnail').hover(
        function(){
            $(this).find('.caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.caption').slideUp(250); //.fadeOut(205)
        });

            $("[rel='tooltip']").tooltip();
});