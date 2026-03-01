$(document).ready(function () {
    var mode = null;


    var getMode = function () {
        return $(window).width() < 768 ? 'small' : 'default';
    };

    var layoutNav = function () {
        var navWidth = $('.sub-nav').width();

        $('.sub-nav').css({
            'left': "-" + navWidth + "px"
        });

    };

    if ($(window).width() < 768) {
        setTimeout(layoutNav, 50);

    }

    $(window).on('resize', function ($state) {
        var new_mode = getMode();
        if (mode != new_mode) {
            window.location.reload();
        }
        if ($(window).width() < 768) {
            layoutNav();
        }
        else if ($(window).width() < 768) {
            $(".tile").css({
                'height': '100%'
            });
        }
    });

    //$(window).on('orientationchange', function (e) {
    //    window.location.reload();
    //});

    mode = getMode();

});




