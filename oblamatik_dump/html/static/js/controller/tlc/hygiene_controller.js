tlcApp.controller('HygieneController', function ($scope, $rootScope, tlcService, $stateParams, $translate, $location) {

    var currentId = $stateParams["tlc_id"];
    $scope.disinfectionRunning = false;
    var statePoll;
    $scope.countDownTime = "";
    $scope.finish_failed = false;

    $('.disinfection-bar').css({
       'background-image':"url('"+$rootScope.routePrefix+"/static/img/tlc_bacterias.png')"
    });

    var pollState = function () {
        tlcService.getTLCState(currentId).then(function (state) {
            state = $rootScope.getSingleElementFromResponse(state);
            var progress = state.progress;

            var barWidth = progress * 100;
            $(".thermal-bar").css({
                width: barWidth + "%"
            });


            $scope.state = state;

            if (state.state == 'g') {

                clearInterval(statePoll);

                $(".thermal-bar").css({
                    'width': '100%'
                });

                $scope.countDownTime = $translate.instant("THERMAL_DESINFECTION_FAILED");
                $scope.finish_failed = true;

            }
            else if (state.state == 'e') {

                clearInterval(statePoll);

                $(".thermal-bar").css({
                    'width': '100%',
                    'background-color': '#99CC00'
                });

                $scope.countDownTime = $translate.instant("THERMAL_DESINFECTION_FINISHED");
                $scope.finish_failed = true;
            }

        });
    };

    $scope.startDisinfection = function () {
        $scope.disinfectionRunning = true;

        tlcService.startDesinfection(currentId);
        statePoll = setInterval(pollState, 1000);
    };

    tlcService.getTLC(currentId).then(function (TLC) {
        $scope.TLC = $rootScope.getTLCFromResponse(TLC);


        //if ($scope.TLC.state == 'b') {
        //    $location.path(currentId + '/home');
        //}
        //else if ($scope.TLC.state == 'c') {
        //    $location.path(currentId + '/warm_up');
        //}
        //else if ($scope.TLC.state == 'h') {
        //    $location.path(currentId + '/bathtub_fill');
        //}
        //
        //if ($scope.TLC.state == 'f') {
        //    statePoll = setInterval(pollState, 1000);
        //    $scope.disinfectionRunning = true;
        //}

        if ($scope.TLC.state == 'g') {


            clearInterval(statePoll);

            $(".thermal-bar").css({
                'width': '100%'
            });

            $scope.countDownTime = $translate.instant("THERMAL_DESINFECTION_FAILED");
            $scope.finish_failed = true;

        }
        else if ($scope.TLC.state == 'e') {

            clearInterval(statePoll);

            $(".thermal-bar").css({
                'width': '100%',
                'background-color': '#99CC00'
            });

            $scope.countDownTime = $translate.instant("THERMAL_DESINFECTION_FINISHED");
            $scope.finish_failed = true;
        }

    });

    tlcService.getTLCState(currentId).then(function (state) {
        state = $rootScope.getSingleElementFromResponse(state);
        var progress = state.progress;


        if (progress != 0) {
            $scope.disinfectionRunning = true;
            statePoll = setInterval(pollState, 1000);

            var barWidth = progress * 100;
            $(".thermal-bar").css({
                width: barWidth + "%"
            });

        }
    });

    $scope.saveHygiene = function () {
        tlcService.setHygieneDetail($scope.hygiene).then(function () {

        });
    };


    tlcService.getHygieneDetail(currentId).then(function (hygiene) {
        $scope.hygiene = $rootScope.getSingleElementFromResponse(hygiene);
        $scope.flushActive = $scope.hygiene.hygiene_flush_active;
        $scope.hygieneFlushActive = $scope.flushActive;
        $scope.repetitionperiod = $scope.hygiene.repetition_period;
        $scope.flushDuration = $scope.hygiene.flush_duration;

        if ($scope.flushActive == false) {
            $scope.repetitionperiod = 7;
            $scope.flushDuration = 10;

        }

        if ($scope.flushDuration == 60) {
            $scope.durationLabel = "1 min";
        }
        else if ($scope.flushDuration == 300) {
            $scope.durationLabel = "5 min";
        }
        else if ($scope.flushDuration == 600) {
            $scope.durationLabel = "10 min";
        }
        else {
            $scope.durationLabel = $scope.flushDuration + " s";
        }


        if ($scope.repetitionperiod == 1) {
            $scope.repetitionperiodLabel = $scope.repetitionperiod + " "+$translate.instant("DAY");
        }
        else {
            $scope.repetitionperiodLabel = $scope.repetitionperiod + " "+$translate.instant("DAYS");
        }

        $scope.flushDurationSeconds = $scope.hygiene.flush_duration;

        window.setTimeout($rootScope.layoutContent, 1);
        window.setTimeout($rootScope.layoutTiles, 1)
    });


    window.setTimeout($rootScope.layoutContent, 1);

    $('.nav-open a').on("click", function () {
        $rootScope.navSlideOut();
    });

    $scope.setRepetitionPeriod = function (period) {
        $scope.hygiene.repetition_period = period;
        $scope.saveHygiene();
        $scope.repetitionperiod = $scope.hygiene.repetition_period;

        if ($scope.repetitionperiod == 1) {
            $scope.repetitionperiodLabel = $scope.repetitionperiod + " "+$translate.instant("DAY");
        }
        else {
            $scope.repetitionperiodLabel = $scope.repetitionperiod + " "+$translate.instant("DAYS");
        }

    };

    $scope.setFlushDuration = function (duration) {


        $scope.hygiene.flush_duration = duration;
        $scope.flushDuration = $scope.hygiene.flush_duration;

        $scope.saveHygiene();

        if (duration == 60) {
            $scope.durationLabel = "1 min";
        }
        else if (duration == 300) {
            $scope.durationLabel = "5 min";
        }
        else if (duration == 600) {
            $scope.durationLabel = "10 min";
        }
        else {
            $scope.durationLabel = duration + " s";
        }
    };

    var saveRequestPending = false;

    var saveTLC = function (changedKey) {

        $scope.sendTLC = {
            "id": $scope.TLC.id,
            "name": $scope.TLC.name,
            "temperature": $scope.TLC.temperature,
            "flow": $scope.TLC.flow,
            "changed": changedKey
        };

        if (!saveRequestPending) {
            saveRequestPending = true;
            tlcService.saveTLC($scope.sendTLC).then(function () {
                saveRequestPending = false;
            });
        }
    };


    var shutDownTLC = function () {

        $scope.TLC.flow = 0;
        $scope.TLC.temperature = 0;

        saveTLC(0);
    };

    window.onbeforeunload = function () {
        shutDownTLC();
        clearInterval(statePoll);
    };


    $scope.$watch('hygieneFlushActive', function (newValue, oldValue) {
        $scope.flushActive = newValue;

        if (oldValue != undefined) {
            $scope.hygiene.hygiene_flush_active = $scope.flushActive;
            $scope.hygiene.repetition_period = $scope.repetitionperiod;
            $scope.hygiene.flush_duration = $scope.flushDuration;
            $scope.saveHygiene();
        }
    });


    $scope.reload = function () {
        window.location.reload();
    };


    $scope.cancelDisinfection = function () {
        $scope.disinfectionRunning = false;

        tlcService.cancelDesinfection(currentId).then(function () {
            window.location.reload();
        });

    };

    $('.tile').on("scroll", function () {
        $('input').toggleClass('force-redraw');
    });

    $scope.okPressed = function () {
        tlcService.cancelDesinfection(currentId).then(function () {
            shutDownTLC();
            $scope.disinfectionRunning = false;
            window.location.reload();
        });

    }

});