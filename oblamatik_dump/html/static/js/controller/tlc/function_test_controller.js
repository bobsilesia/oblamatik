tlcApp.controller('FunctionTestController', function ($scope, $rootScope, tlcService, $stateParams, $translate, $location) {

    window.setTimeout($rootScope.layoutContent, 1);

    var tlc_id = $stateParams['tlc_id'];
    $scope.TLCid = tlc_id;
    var statePoll;
    var currentId = $stateParams["tlc_id"];
    var restarting = true;

    var pollState = function () {
        if (restarting == true) {
            $scope.functionTestFirstStep();
        }
        tlcService.getTLCState(currentId).then(function (state) {
            state = $rootScope.getSingleElementFromResponse(state);

            if (state.state == 'b') {
                restarting = false;
                $('.controller-ready').show();
                $('.controller-restart').hide();

                $('.progress-bar').finish();

                $('#ft-first-step').show();

            }
        });
    };

    tlcService.getTLCState(currentId).then(function (state) {
        state = $rootScope.getSingleElementFromResponse(state);
        $scope.function_test = state.function_test;
        if (state.function_test != 0) {
            statePoll = setInterval(pollState, 1000);
            $scope.functionTestRunning = true;

            if (state.function_test >= 1) {
                $('#ft-first-step').show();
            }

            if (state.function_test >= 2) {
                $scope.FTStep1_1 = true;
                $scope.FTStep1_2 = true;
            }
            if (state.function_test >= 3) {
                $scope.FTStep2_1 = true;
                $scope.FTStep2_2 = true;
            }
            if (state.function_test >= 4) {
                $scope.FTStep3_1 = true;
                $scope.FTStep3_2 = true;
                $scope.functionTestRunning = false;
            }

        }

    });

    $scope.functionTestRunning = false;
    $('.controller-ready').hide();
    $('#ft-first-step').hide();
    $scope.FTStep1_1 = null;
    $scope.FTStep1_2 = null;
    $scope.FTStep2_1 = null;
    $scope.FTStep2_2 = null;
    $scope.FTStep3_1 = null;
    $scope.FTStep3_2 = null;

    $scope.functionTestFirstStep = function () {
        tlcService.functionTestStep1(tlc_id).then(function () {
        });
    };


    $scope.functionTestThirdStep = function () {
        tlcService.functionTestStep3(tlc_id).then(function () {
            $scope.FTStep2_2 = true;
        });
    };

    $scope.functionTestSecondStep = function () {
        tlcService.functionTestStep2(tlc_id).then(function () {
            $scope.FTStep1_2 = true;
        });
    };

    $scope.startFunctionTest = function () {
        $('.controller-ready').hide();
        $('#ft-first-step').hide();
        $scope.FTStep1_1 = null;
        $scope.FTStep1_2 = null;
        $scope.FTStep2_1 = null;
        $scope.FTStep2_2 = null;
        $scope.FTStep3_1 = null;
        $scope.FTStep3_2 = null;
        $('.progress-bar').css({
            'width': '0%'
        });

        var state = {'state': 1};

        tlcService.savePopUpState($scope.TLC.id, state);

        statePoll = setInterval(pollState, 1000);
        tlcService.functionTestStep0(tlc_id).then(function () {

        });

        restarting = true;

        $('.progress-bar').animate({
            width: '100%'
        }, 12000, 'linear', function () {

        });

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

    $scope.cancelFunctionTest = function () {
        shutDownTLC();
        clearInterval(statePoll);

    };

    $scope.cancelButtonPressed = function () {
        shutDownTLC();
        clearInterval(statePoll);
        window.location.reload();
    };

    $scope.functionTestFinished = function () {
        $scope.functionTestRunning = false;
        clearInterval(statePoll);
        shutDownTLC();
    };


    $('.selection-inactive').on('click', function () {
        return false;
    });

    $('.nav-open a').on("click", function () {
        $rootScope.navSlideOut();
    });


    tlcService.getTLC(currentId).then(function (TLC) {
        $scope.TLC = $rootScope.getTLCFromResponse(TLC);
        window.setTimeout($rootScope.layoutContent, 1);
        window.setTimeout($rootScope.layoutTiles, 1);

        //if ($scope.TLC.state == 'b') {
        //    if ($scope.function_test == 0) {
        //        $location.path(currentId + '/home');
        //    }
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
    });
});