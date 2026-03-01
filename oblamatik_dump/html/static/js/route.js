tlcApp.config(function ($stateProvider, $urlRouterProvider) {
    //
    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/");
    //
    var routePrefix = $("routePrefix").attr("href");

    if ($(window).width() < 768) {
        $stateProvider
            .state('home', {
                url: "/",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/home.html",
                        controller: 'HomeController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('tlc_home', {
                url: "/:tlc_id/home",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/tlc_home.html",
                        controller: 'TLCHomeController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('function_test', {
                url: "/:tlc_id/function_test",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/function_test.html",
                        controller: 'FunctionTestController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('warm_up', {
                url: "/:tlc_id/warm_up",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/warm_up.html",
                        controller: 'WarmUpController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('info', {
                url: "/:tlc_id/info",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/info.html",
                        controller: 'InfoController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('settings', {
                url: "/:tlc_id/settings",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/settings.html",
                        controller: 'SettingsController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('network', {
                url: "/:tlc_id/network",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/network.html",
                        controller: 'NetworkController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('hygiene', {
                url: "/:tlc_id/hygiene",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/hygiene.html",
                        controller: 'HygieneController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('bathtub_fill', {
                url: "/:tlc_id/bathtub_fill",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/bathtub_fill.html",
                        controller: 'BathtubFillController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('measuring_cup', {
                url: "/:tlc_id/measuring_cup",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/measuring_cup.html",
                        controller: 'MeasuringCupController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('quick_bath_fill', {
                url: "/:tlc_id/quick_bath_fill",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/quick_bathtub_fill.html",
                        controller: 'QuickBathController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
            .state('password', {
                url: "/:tlc_id/password",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/password.html",
                        controller: 'PasswordController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/sub_menu.html",
                        controller: 'SubmenuController'
                    }
                }
            })
    }
    else {
        $stateProvider
            .state('home', {
                url: "/",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/home.html",
                        controller: 'HomeController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('tlc_home', {
                url: "/:tlc_id/home",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/tlc_home.html",
                        controller: 'TLCHomeController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('function_test', {
                url: "/:tlc_id/function_test",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/function_test.html",
                        controller: 'FunctionTestController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('warm_up', {
                url: "/:tlc_id/warm_up",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/warm_up.html",
                        controller: 'WarmUpController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('info', {
                url: "/:tlc_id/info",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/info.html",
                        controller: 'InfoController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('settings', {
                url: "/:tlc_id/settings",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/settings.html",
                        controller: 'SettingsController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('network', {
                url: "/:tlc_id/network",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/network.html",
                        controller: 'NetworkController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('hygiene', {
                url: "/:tlc_id/hygiene",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/hygiene.html",
                        controller: 'HygieneController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('bathtub_fill', {
                url: "/:tlc_id/bathtub_fill",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/bathtub_fill.html",
                        controller: 'BathtubFillController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('measuring_cup', {
                url: "/:tlc_id/measuring_cup",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/measuring_cup.html",
                        controller: 'MeasuringCupController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('quick_bath_fill', {
                url: "/:tlc_id/quick_bath_fill",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/quick_bathtub_fill.html",
                        controller: 'QuickBathController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
            .state('password', {
                url: "/:tlc_id/password",
                views: {
                    "content": {
                        templateUrl: routePrefix + "templates/tlc/password.html",
                        controller: 'PasswordController'
                    },
                    "menu": {
                        templateUrl: routePrefix + "templates/menus/main_menu.html",
                        controller: 'MainMenuController'
                    }
                }
            })
    }


});

