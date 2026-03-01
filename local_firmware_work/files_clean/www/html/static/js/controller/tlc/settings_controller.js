tlcApp.controller('SettingsController', function ($scope, $rootScope, tlcService, $stateParams, $translate, $location) {

    var currentId = $stateParams["tlc_id"];

    //for (var i = 1; i < 99999; i++) {
    //    window.clearInterval(i);
    //}

    $scope.minimalTemp = 4;
    $scope.maximalTemp = 80;


    tlcService.getTLC(currentId).then(function (TLC) {
        $scope.TLC = $rootScope.getTLCFromResponse(TLC);

        $scope.TLC.name = he.decode($scope.TLC.name);

        //if ($scope.TLC.state == 'b') {
        //    $location.path(currentId + '/home');
        //}
        //else if ($scope.TLC.state == 'c') {
        //    $location.path(currentId + '/warm_up');
        //}
        //else if ($scope.TLC.state == 'f' || $scope.TLC.state == 'g' || $scope.TLC.state == 'e') {
        //    $location.path(currentId + '/hygiene');
        //}
        //else if ($scope.TLC.state == 'h') {
        //    $location.path(currentId + '/bathtub_fill');
        //}

        window.setTimeout($rootScope.layoutContent, 1);
        window.setTimeout($rootScope.layoutTiles, 1)
    });

    tlcService.getTLCSettings(currentId).then(function (settings) {
        $scope.settings = $rootScope.getSingleElementFromResponse(settings);

        $scope.currentAmbient = $scope.settings.ambient_light;
        $scope.setAmbientColor($scope.settings.ambient_light);

        $scope.tempConversionType = $scope.settings.temperature_unit;

        if ($scope.tempConversionType == 0) {
            $scope.tempCurrency = '°C';

            $scope.minimalTemp = 4;
            $scope.maximalTemp = 80;
            $scope.maxTemp = $scope.settings.max_temp;
        }
        else {
            $scope.tempCurrency = '°F';

            $scope.minimalTemp = 4 * 1.8 + 32;
            $scope.maximalTemp = 80 * 1.8 + 32;
            $scope.maxTemp = $scope.settings.max_temp * 1.8 + 32;
        }

        $scope.maxRuntime = $scope.settings.max_flow_time;


    });

    var saveSettings = function () {
        tlcService.saveTLCSettings($scope.settings).then(function () {

        });
    };

    $scope.setTempUnit = function (unit) {
        if (unit == 0) {
            $scope.tempCurrency = '°C';
        }
        else {
            $scope.tempCurrency = '°F';
        }

        $scope.tempConversionType = $scope.settings.temperature_unit = unit;

        if ($scope.tempConversionType == 0) {
            $scope.tempCurrency = '°C';

            $scope.minimalTemp = 4;
            $scope.maximalTemp = 80;
            $scope.maxTemp = Math.round($scope.settings.max_temp);
            $('#maxTemp').val($scope.maxTemp);
        }
        else {
            $scope.tempCurrency = '°F';

            $scope.minimalTemp = 4 * 1.8 + 32;
            $scope.maximalTemp = 80 * 1.8 + 32;
            $scope.maxTemp = Math.round($scope.settings.max_temp * 1.8 + 32);
            $('#maxTemp').val($scope.maxTemp);
        }

        saveSettings();
    };

    $scope.getAmbientColor = function (ambientKey) {
        switch (ambientKey) {
            case 0:
                return '#848484';
                break; //grau
            case 1:
                return '#00DDFF';
                break; //cyan
            case 2:
                return '#0059A1';
                break; //blau
            case 3:
                return '#ff0090';
                break; //magenta
            case 4:
                return '#E30514';
                break; //rot
            case 5:
                return '#ED6E03';
                break; //orange
            case 6:
                return '#FEF000';
                break; //gelb
            case 7:
                return '#3BA534';
                break; //grün
            case 8:
                return '#FFFFFF';
                break; //weiss
            case 9:
                return '#646464';
                break; //ambient
        }
    };

    $scope.getAmbientKey = function (ambientKey) {
        switch (ambientKey) {
            case 0:
                return 'BLACK';
                break; //schwarz
            case 1:
                return 'LIGHT_BLUE';
                break; //hellblau
            case 2:
                return 'BLUE';
                break; //blau
            case 3:
                return 'PINK';
                break; //pink
            case 4:
                return 'RED';
                break; //rot
            case 5:
                return 'ORANGE';
                break; //orange
            case 6:
                return 'YELLOW';
                break; //gelb
            case 7:
                return 'GREEN';
                break; //grün
            case 8:
                return 'WHITE';
                break; //weiss
            case 9:
                return 'AMBIENT_LIGHT';
                break; //ambient
        }
    };

    var ambientTrans;

    $scope.setAmbientColor = function (ambient) {
        $scope.settings.ambient_light = ambient;
        saveSettings();

        if (ambient != 9) {
            var ambientColor = $scope.getAmbientColor(ambient);

            ambientTrans = $scope.getAmbientKey(ambient);

            $scope.ambientName = $translate.instant(ambientTrans);

            $('.ambient-light-tile').css({
                'background': ambientColor
            });

            if (ambientColor == '#848484' ||
                ambientColor == '#0059A1' ||
                ambientColor == '#E30514' ||
                ambientColor == '#ff0090') {
                $('.ambient-light-tile button').css({
                    'color': '#FFFFFF'
                });
            }
            else {
                $('.ambient-light-tile button').css({
                    'color': '#000000'
                });
            }
        }
        else {
            ambientTrans = $scope.getAmbientKey(ambient);
            $scope.ambientName = $translate.instant(ambientTrans);

            $('.ambient-light-tile').css({
                'background': $('#ambient_light').css('background')
            });


        }

    };
    var ambientColor = $scope.getAmbientColor($scope.currentAmbient);

    $scope.restartDevice = function () {
        tlcService.functionTestStep0($scope.TLC.id);
    };

    $('.tile').on("click", function () {
        if ($scope.status.isopen == true) {
            $scope.status.isopen = false;
        }
    });

    $('#maxTemp').on('change', function () {
        if ($(this).val() >= $scope.minimalTemp && $(this).val() <= $scope.maximalTemp) {
            if ($scope.tempConversionType == 0) {
                $scope.settings.max_temp = $(this).val();
            }
            else {
                $scope.settings.max_temp = ($(this).val() - 32) / 1.8;
            }

            saveSettings();

            $(this).css({
                'border-color': ''
            })
        }
        else {
            $(this).css({
                'border-color': 'red'
            })
        }
    });

    $('#maxRuntime').on('change', function () {
        if ($(this).val() >= 1 && $(this).val() <= 99) {
            $scope.maxRuntime = $scope.settings.max_flow_time = $(this).val();
            saveSettings();

            $(this).css({
                'border-color': ''
            })
        }
        else {
            $(this).css({
                'border-color': 'red'
            })
        }
    });


    $('.ambient-light-tile').css({
        'background-color': ambientColor
    });

    if ((ambientColor == '#848484' ||
        ambientColor == '#0059A1' ||
        ambientColor == '#E30514' ||
        ambientColor == '#ff0090')) {
        $('.ambient-light-tile button').css({
            'color': '#FFFFFF'
        });
    }
    else {
        $('.ambient-light-tile button').css({
            'color': '#000000'
        });
    }

    $('.nav-open a').on("click", function () {
        $rootScope.navSlideOut();
    });

    $('.device-name').on("keyup", function (evt) {
        $scope.TLC.name = $(this).val();

        var device_name = he.encode($scope.TLC.name);

        $('.selected .text-span').text($scope.setEliptedString($(this).val()));
        $('#category-header .ng-binding').text($scope.setEliptedString($(this).val()));

        $scope.sendTLC = {
            "id": $scope.TLC.id,
            "name": device_name,
            "temperature": $scope.TLC.temperature,
            "flow": $scope.TLC.flow,
            "changed": 3
        };

        tlcService.saveTLC($scope.sendTLC);


        if (evt.which == 13) {
            $(this).blur();
        }
    });

    $('.number-input input').on("keyup", function (evt) {
        if (evt.which == 13) {
            $(this).blur();
        }
    });

    $('.tile').on("scroll", function () {
        $('input').toggleClass('force-redraw');
    });

});