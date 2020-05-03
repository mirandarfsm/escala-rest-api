(function() {
    'use strict';

    angular
        .module("Escalante")
        .config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        $routeProvider
            .when('/404', {
                templateUrl: 'app/error/error.html',
                controller: 'ErrorController',
                controllerAs: 'vm',
                resolve: {
                    error404: error404
                }
            })
            .otherwise({
                redirectTo: '/404'
            });
    }

    function error404() {
        return true
    }

})();