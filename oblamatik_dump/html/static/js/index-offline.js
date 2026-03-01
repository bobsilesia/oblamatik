var tlcApp = angular.module('tlcApp', ['ngAnimate', 'ngCookies', 'angular-md5', 'ui.router', 'ui.bootstrap', 'frapontillo.bootstrap-switch', 'pascalprecht.translate', 'ngFileUpload', 'ngWebSocket']);

tlcApp.controller('MainController', function ($scope, $rootScope, $location, $translate, $websocket, $q, $http, tlcService) {

    $rootScope.isTest = false;
    $rootScope.global_server_path = '/api/';//'http://localhost:8000/api/'; //'https://tlc-api.impac.ch/api/'
    $rootScope.hasSocket = false;
    $rootScope.routePrefix = $("routePrefix").attr("href");


    var userLang = navigator.language || navigator.userLanguage;
    $rootScope.tempUnit = '';
    $rootScope.landscape = false;
    $('.wheel-glow').hide();

    function layoutShadowPolygon() {
        var polygon = $('.temp-shadow polygon').get(0);
        var polygon2 = $('.temp-shadow polygon').get(1);
        var polygon3 = $('.temp-shadow polygon').get(2);

        var offsetTile = $('.tile').offset();
        var offsetButton = $('.wheel-interface').offset();
        var widthButton = $('.wheel-interface').width();
        var heightButton = $('.wheel-button').height();


        if (offsetButton !== undefined) {
            var shadowLeft = offsetButton.left - offsetTile.left;
            var shadowTop = offsetButton.top - offsetTile.top;
            var rectangularLength = 900;

            var newX = (widthButton / 2 * Math.cos(33 * Math.PI / 180)) + widthButton / 2;
            var newY = (widthButton / 2 * Math.sin(33 * Math.PI / 180)) + widthButton / 2;

            var point1 = {"x": widthButton - newX, "y": ((heightButton / 4) * 3)};
            var point4 = {"x": newX, "y": (heightButton / 4)};
            var point2 = {
                "x": point1.x + (Math.sin(Math.PI * 33 / 180.0) * rectangularLength),
                "y": point1.y + (Math.cos(Math.PI * 33 / 180.0) * rectangularLength)
            };
            var point3 = {
                "x": point4.x + (Math.sin(Math.PI * 33 / 180.0) * rectangularLength),
                "y": point4.y + (Math.cos(Math.PI * 33 / 180.0) * rectangularLength)
            };

            $(".temp-shadow").css({
                "left": shadowLeft + "px",
                "top": shadowTop + "px"
            });


            polygon.setAttribute("points", "" + point1.x + "," + point1.y + " " + point2.x + "," + point2.y + " " + point3.x + "," + point3.y + " " + point4.x + "," + point4.y + "");
            if (polygon2 != undefined) {
                polygon2.setAttribute("points", "" + point1.x + "," + point1.y + " " + point2.x + "," + point2.y + " " + point3.x + "," + point3.y + " " + point4.x + "," + point4.y + "");
            }
            if (polygon3 != undefined) {
                polygon3.setAttribute("points", "" + point1.x + "," + point1.y + " " + point2.x + "," + point2.y + " " + point3.x + "," + point3.y + " " + point4.x + "," + point4.y + "");
            }
        }
    }


    function glowLayout(diameter, tileHeight, wheelTopOffset) {
        $('.wheel-glow').width(diameter * 1.313);
        $('.wheel-glow').height(diameter * 1.38);
        $('.wheel-glow').css({
            'left': $('.tile').width() / 2 - $('.wheel-glow').width() / 2,
            'top': (tileHeight / 2) - ($('.wheel-glow').height() / 2) + wheelTopOffset
        });
    }

    function portraitLayout() {
        var switchWidth = $('.temp-slider').width() + $('.icon-waterflow').width() + $('.icon-thermostat').width();
        var switchLeft = $(window).width() / 2 - switchWidth / 2 - 3;
        var windowHeight = $('.tile').height();
        var modeSelectionBottom = (windowHeight - $('#temp').offset().top - $('#temp').height()) / 2 + 25; // 25: half header height;
        var valueDisplayTop = $('#temp').offset().top / 2 - 50; // 50 : header height

        $('.mode-selection').css({
            'left': switchLeft,
            'top': valueDisplayTop
        });

        $('.value-display').css({
            'top': 'auto',
            'bottom': modeSelectionBottom
        });

        $rootScope.landscape = false;
    }

    function landscapeLayout() {
        var modeSelection = $('.temp-slider').height();
        var windowHeight = $('.tile').height();
        var windowWidth = $(window).width();

        $('.mode-selection').css({
            'top': windowHeight / 2 - modeSelection / 2 - 25,
            'left': '20px'
        });


        $('.value-display').css({
            'right': 0,
            'width': ($('.tile').width() - $('.wheel-interface').width()) / 2,
            'top': 0,
            'height': windowHeight - $('.mobile-header').height(),
            'margin': 0,
            'left': 'auto'
        });

        $rootScope.landscape = true;
    }

    function setWheelTop(tileHeight, wheelTopOffset, diameter) {
        var wheelTop = (tileHeight / 2) - ($('.wheel-button').height() / 2) + wheelTopOffset;

        $('.wheel-button').css({
            'top': wheelTop,
            'transform': 'none'
        });
        if (tileHeight < 520) {
            $('.wheel-button').width(diameter);
            $('.wheel-button').height(diameter * 1.09);

            $('.wheel-button').css({
                'top': wheelTop + 15,
                'transform': 'none'
            });
        }
    }

    function getDiameter(tileHeight, diameter) {
        if (tileHeight < 520) {
            return diameter - 30;
        }
        else {
            return diameter;
        }
    }


    $rootScope.tlc_base_layout = function () {
        var tileWidth = $('.tile').width();
        var tileHeight = $('.tile').height();
        var x = Math.min(tileWidth, tileHeight);
        var diameter = Math.min(0.8 * x, Math.sqrt(180 * x));
        $('.wheel-button').width(diameter);
        $('.wheel-button').height(diameter * 1.09);

        $('.wheel-button').show();

        var wheelTopOffset;
        if ($(window).width() < 768) {
            wheelTopOffset = (-20);
        }
        else {
            wheelTopOffset = 10;
        }

        if ($('.wheel-button').height() > 50) {
            diameter = getDiameter(tileHeight, diameter);
            setWheelTop(tileHeight, wheelTopOffset, diameter);
            glowLayout(diameter, tileHeight, wheelTopOffset);

            layoutShadowPolygon();
            if ($(window).width() < 768) {
                if (Math.abs(window.orientation) === 90) {
                    landscapeLayout();
                } else {
                    portraitLayout();
                }
            }
        }
        else {
            window.setTimeout($rootScope.tlc_base_layout, 300);
        }
    };

    var loadingTimeout;

    function handleError(response) {
        clearTimeout(loadingTimeout);
        $("#loading-view").hide();

        if (
            !angular.isObject(response.data) || !response.data.message
        ) {

            return ( $q.reject("An unknown error occurred.") );
        }

        return ( $q.reject(response.data.message) );

    }

    function handleSuccess(response) {
        clearTimeout(loadingTimeout);
        loadingTimeout = undefined;
        $("#loading-view").hide();
        return ( response.data );

    }

    function parseGroupSocketInfo() {
        if ($.cookie("channels_and_secrets") !== undefined) {
            var to_escape = $.cookie("channels_and_secrets");
            var unescaped = to_escape.replace(/\\054/g, ",");
            $rootScope.iots = JSON.parse(unescaped);
        }
    }

    function createWebSockets() {
        var channel = $.cookie("channel");
        var secret = $.cookie("secret");
        var host = $.cookie("host");
        var socketWS = 'wss';
        if (host.indexOf("localhost") > -1) {
            socketWS = 'ws'
        }
        if (channel == undefined || secret == undefined) {
            window.location.href = "/"
        }
        // $rootScope.socketSecret = secret;
        // $rootScope.webSocket = $websocket(socketWS + '://' + host + '/ws/' + channel + '?subscribe-broadcast&publish-broadcast');
        // $rootScope.webSocket.reconnectIfNotNormalClose = true;

        $rootScope.webSockets = {};
        $rootScope.socketSecrets = {};
        angular.forEach($rootScope.iots, function (iot, id) {
            $rootScope.webSockets[id] = $websocket(socketWS + '://' + host + '/ws/' + iot["channel"] + '?subscribe-broadcast&publish-broadcast');
            $rootScope.webSockets[id].reconnectIfNotNormalClose = true;
            $rootScope.socketSecrets[id] = iot["secret"];
        });
    }

    if ($rootScope.hasSocket) {

        parseGroupSocketInfo();
        createWebSockets();

        var handleResponse = function (event) {
            if (event.data != "ping") {
                var data = angular.fromJson(event.data);

                console.log("Receive", data.id, "<----");
                console.dir(data);
                console.log("---->");

                if (angular.isDefined($rootScope.callbacks[data.id])) {
                    var callback = $rootScope.callbacks[data.id];
                    //delete $rootScope.callbacks[data.id];
                    callback.resolve(data);
                } else {
                    console.log("Skip", data.id);
                    //console.log("Don't send old responses :@: %o", data);
                }
            }
        }

        //$rootScope.webSocket.onMessage(function (event) {
        //    // main channel
        //    handleResponse(event);
        //});

        $rootScope.callbacks = {};

        angular.forEach($rootScope.iots, function (iot, id) {
            $rootScope.webSockets[id].onMessage(function (event) {
                // per iot channel
                handleResponse(event);
            });
        });

        $rootScope.$on("$locationChangeStart", function (event, next, current) {
            if ($.cookie("update_required") == "True") {
                $location.path("settings/versions");
            }
        });

        var hasUpdate = $.cookie("has_update");
        if (hasUpdate == "True") {
            $.removeCookie('has_update', {path: '/'});
            $location.path("settings/versions");
        }

    }

    // initialize with a random postfix
    var requestId = Math.floor((Math.random() * 8999) + 1000);
    $rootScope.getRequestId = function () {
        requestId = requestId + 100000;
        return requestId;
    };

    function sendSocketMessage(url, method, data, tlcID) {
        var full_url = '/api/' + url;
        var hashElements = full_url + $rootScope.socketSecrets[tlcID];
        var hash = CryptoJS.SHA512(hashElements).toString(CryptoJS.enc.Hex);

        var request = {
            'id': $rootScope.getRequestId(),
            'url': full_url,
            'method': method,
            'hash': hash,
            'data': data,
            'tlcID': tlcID
        };
        var d = $q.defer();
        $rootScope.callbacks[request.id] = d;

        $rootScope.webSockets[tlcID].send(angular.toJson(request));
        console.log("Send", request.id, method, url, tlcID, "--->");
        console.dir(request);
        return d.promise;
    }

    $rootScope.$on("$locationChangeStart", function (event, next, current) {
        var interval_id = window.setInterval(function () {
        }, 9999); // Get a reference to the last
        for (var i = 1; i < interval_id; i++) {
            window.clearInterval(i);
        }
    });

    $rootScope.request = function (url, method, data, tlcID) {
        var header = undefined;
        var new_data = undefined;
        var request = undefined;

        if ($rootScope.hasSocket) {

            if (tlcID !== undefined) {
                // Wenn Request an ein bestimmtes Gerät gesendet werden soll
                return sendSocketMessage(url, method, data, tlcID);
            } else {
                // Wenn Request an alle Geräte gesendet werden soll
                var promises = [];
                angular.forEach($rootScope.iots, function (iot, tlcID) {
                    promises.push(
                        sendSocketMessage(url, method, data, tlcID)
                    );
                });
                return $q.all(promises);
            }

        } else {

            if ($rootScope.isTest) {
                new_data = data;
            }
            else if (data != undefined && !$rootScope.isTest) {
                new_data = $.param(data);
                header = {'Content-Type': 'application/x-www-form-urlencoded'};
            }

            if (method == 'POST') {
                request = $http({
                    method: method,
                    data: new_data,
                    headers: header,
                    url: $rootScope.global_server_path + url + '?q=' + Math.random()
                });
            } else {
                request = $http({
                    method: method,
                    url: $rootScope.global_server_path + url + '?q=' + Math.random()
                });
            }

            return ( request.then(handleSuccess, handleError) );
        }

    };


    if (userLang.length != 2) {
        userLang = userLang.slice(0, 2);
    }

    $scope.setEliptedString = function (str) {


        if (str != undefined) {

            str = he.decode(str);

            if (str.length > 12) {
                return str.substr(0, 4) + '...' + str.substr(str.length - 4, str.length);
            }
            return str;
        }

    };

    var availableTranslations = ["en", "de"];

    var inArray = $.inArray(userLang, availableTranslations);
    if (inArray != -1) {
        $translate.use(userLang);
    }
    else {
        $translate.use("en");
    }


    $rootScope.layoutTiles = function () {
        var prev = $('.tile').height();
        $(".tile").css({
            'height': '100%'
        });
        if ($('.tile').height() == 0) {
            $('.tile').height(prev);
        }

        var tileTitle = 0;

        if ($(window).width() >= 768 && $(window).width() >= 992) {
            tileTitle = 0;
            if ($('.tile').height() > $(window).height() - 400) {
                tileTitle = 85;
            }

        }
        else if ($(window).width() >= 768 && $(window).width() <= 992) {
            if ($('.tile').height() <= $(window).height() / 2) {
                tileTitle = 10;
            }
            else if ($('.tile').height() > $(window).height() / 2) {
                tileTitle = 85;
            }
        }

        $(".tile").height($(".tile").height() - tileTitle);

        if ($('.wheel-button').height() !== null) {
            $scope.tlc_base_layout();
        }


    };

    $(window).on('orientationchange', function (e) {
        window.location.reload();
    });

    $rootScope.getTLCsFromResponse = function (response) {
        var arr = [];
        if ($rootScope.hasSocket) {
            angular.forEach(response, function (tlc, key) {
                angular.forEach(tlc.data, function (tlcdata, key) {
                    tlcdata.id = tlc.tlcID;
                    arr.push(tlcdata);
                });
            });
            return arr;
        } else {
            return response;
        }
    };

    $rootScope.getTLCFromResponse = function (tlc) {
        if ($rootScope.hasSocket) {
            tlc = tlc.data;
        }
        return tlc;
    };

    $rootScope.getSingleElementFromResponse = function (response) {
        if ($rootScope.hasSocket) {
            response = response.data;
        }
        return response;
    };

    $rootScope.navSlideOut = function () {
        $('.menu').stop(true, true).animate({
            right: "0"
        }, 500, function () {
            // Animation complete.
        });
    };

    $rootScope.navSlideIn = function () {
        var navWidth = $('.menu').width();

        $('.menu').animate({
            right: "-" + navWidth + "px"
        }, 500, function () {
            // Animation complete.
        });
    };

    $rootScope.slideIn = function (flag) {
        if (flag) {
            $rootScope.navSlideIn();
        }
    }

    $(window).on('resize', function ($state) {
        $rootScope.layoutTiles();
        //if ($(window).width() > 768) {
        //    $rootScope.layoutTiles();
        //}
        //else if ($(window).width() > 992) {
        //    $rootScope.layoutTiles();
        //}
        //else if ($(window).width() < 768) {
        //    $(".tile").css({
        //        'height': '100%'
        //    });
        //}
    });

    //uses document because document will be topmost level in bubbling
    $(document).on('touchmove', function (e) {
        e.preventDefault();
    });
//uses body because jquery on events are called off of the element they are
//added to, so bubbling would not work if we used document instead.
    $('body').on('touchstart', '.tile, .dropdown-menu, .main-content, #navigation', function (e) {
        if (e.currentTarget.scrollTop === 0) {
            e.currentTarget.scrollTop = 1;
        } else if (e.currentTarget.scrollHeight === e.currentTarget.scrollTop + e.currentTarget.offsetHeight) {
            e.currentTarget.scrollTop -= 1;
        }
    });
//prevents preventDefault from being called on document if it sees a scrollable div
    $('body').on('touchmove', '.tile, .dropdown-menu, .main-content, #navigation', function (e) {
        e.stopPropagation();
    });

    tlcService.getTLCs().then(function (TLCs) {
        $rootScope.TLCs = $rootScope.getTLCsFromResponse(TLCs);
        if ($location.path().length <= 1) {
            // redirect from index to appropriate tlc start page
            var firstChildID = $rootScope.TLCs[0].id;
            if ($rootScope.TLCs[0].type == 3) {
                var joinedURL = '/' + firstChildID + "/warm_up";
            } else {
                var joinedURL = '/' + firstChildID + "/home";
            }
            $location.path(joinedURL);
        }


        $rootScope.isVersionOutdated = function (input, currentVersion) {

            if (currentVersion != undefined) {

                var splitted_current_versions = currentVersion.split("-");
                var splitted_iot_versions = input.split("-");
                if (splitted_current_versions.length != 2 || splitted_iot_versions.length != 2) {
                    return false;
                } else {

                    if ($rootScope.newVersionAvailable(splitted_iot_versions[0], splitted_current_versions[0]) || $rootScope.newVersionAvailable(splitted_iot_versions[1], splitted_current_versions[1])) {
                        return true;
                    }

                    return false;
                }
            }
        };

        $rootScope.newVersionAvailable = function (device_version, server_version) {

            var device_version_splitted = device_version.split(".");
            var server_version_splitted = server_version.split(".");

            if (parseInt(device_version_splitted[0]) < parseInt(server_version_splitted[0])) {
                return true;
            }

            if (parseInt(device_version_splitted[0]) <= parseInt(server_version_splitted[0]) && parseInt(device_version_splitted[1]) < parseInt(server_version_splitted[1])) {
                return true;
            }

            return false;
        };
        angular.forEach($rootScope.TLCs, function (tlc, key) {
            var index = $rootScope.TLCs.indexOf(tlc);
            if ($rootScope.isVersionOutdated(tlc.version, tlc.version_number_downloaded)) {
                $rootScope.TLCs[index].updateAvailable = true;
            }
        });


    });

});

function getColorArray(temperature) {
    var mappings = [
        {
            temp: 4,
            r: 0,
            g: 0,
            b: 255
        },
        {
            temp: 6,
            r: 0,
            g: 0,
            b: 255
        },
        {
            temp: 8,
            r: 0,
            g: 0,
            b: 255
        },
        {
            temp: 10,
            r: 0,
            g: 17,
            b: 255
        },
        {
            temp: 12,
            r: 51,
            g: 34,
            b: 255
        },
        {
            temp: 14,
            r: 68,
            g: 34,
            b: 255
        },
        {
            temp: 16,
            r: 68,
            g: 51,
            b: 255
        },
        {
            temp: 18,
            r: 102,
            g: 51,
            b: 255
        },
        {
            temp: 20,
            r: 136,
            g: 85,
            b: 255
        },
        {
            temp: 22,
            r: 221,
            g: 119,
            b: 255
        },
        {
            temp: 24,
            r: 255,
            g: 187,
            b: 255
        },
        {
            temp: 26,
            r: 255,
            g: 221,
            b: 204
        },
        {
            temp: 28,
            r: 255,
            g: 204,
            b: 85
        },
        {
            temp: 30,
            r: 255,
            g: 187,
            b: 34
        },
        {
            temp: 32,
            r: 255,
            g: 187,
            b: 0
        },
        {
            temp: 34,
            r: 255,
            g: 153,
            b: 0
        },
        {
            temp: 36,
            r: 255,
            g: 136,
            b: 0
        },
        {
            temp: 38,
            r: 255,
            g: 119,
            b: 0
        },
        {
            temp: 40,
            r: 255,
            g: 102,
            b: 0
        },
        {
            temp: 42,
            r: 255,
            g: 85,
            b: 0
        },
        {
            temp: 44,
            r: 255,
            g: 68,
            b: 0
        },
        {
            temp: 46,
            r: 255,
            g: 51,
            b: 0
        },
        {
            temp: 48,
            r: 255,
            g: 34,
            b: 0
        },
        {
            temp: 50,
            r: 255,
            g: 17,
            b: 0
        },
        {
            temp: 52,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 54,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 56,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 58,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 60,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 62,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 64,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 66,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 68,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 70,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 72,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 74,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 76,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 78,
            r: 255,
            g: 0,
            b: 0
        },
        {
            temp: 80,
            r: 255,
            g: 0,
            b: 0
        }
    ];

    var rgb = {
        r: 0,
        g: 0,
        b: 0
    };

    if (temperature < 4) {
        rgb = mappings[0];
    }
    else if (temperature >= 80) {
        rgb = mappings[mappings.length - 1];
    }
    else {
        var indexLow = Math.floor((temperature - 4) / 2);
        var step = (temperature - 4) / 2 - indexLow;

        rgb.r = Math.round((1 - step) * (mappings[indexLow].r) + (step * (mappings[indexLow + 1].r)));
        rgb.g = Math.round((1 - step) * (mappings[indexLow].g) + (step * (mappings[indexLow + 1].g)));
        rgb.b = Math.round((1 - step) * (mappings[indexLow].b) + (step * (mappings[indexLow + 1].b)));
    }

    return rgb;
}

function getHexColorFromColor(color) {
    var red = color.r.toString(16);
    if (red.length == 1) {
        red = "0" + red;
    }

    var green = color.g.toString(16);
    if (green.length == 1) {
        green = "0" + green;
    }

    var blue = color.b.toString(16);
    if (blue.length == 1) {
        blue = "0" + blue;
    }

    return "#" + red + green + blue;
}