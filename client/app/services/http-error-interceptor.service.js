(function() {
    'use strict';

    angular
        .module('Escalante')
        .factory('httpErrorInterceptor', httpErrorInterceptor);

    httpErrorInterceptor.$inject = ['$q', '$location', 'alertService'];

    function httpErrorInterceptor($q, $location, alertService) {

        var service = {
            responseError: responseError
        }

        function responseError(response) {
            let httpErrorResponse = response.data;
            switch (httpErrorResponse.status) {
                case 0:
                    alertService.addError('Server not reachable');
                    break;

                case 400:
                    alertService.addError(httpErrorResponse.message);
                    break;

                case 401:
                    $location.path('/login');
                    break;

                case 404:
                    alertService.addError('Not found');
                    break;

                default:
                    if (httpErrorResponse.error !== '' && httpErrorResponse.error.message) {
                        alertService.addError(httpErrorResponse.error.message);
                    } else {
                        alertService.addError(httpErrorResponse.error);
                    }
            }
            return $q.reject(httpErrorResponse)
        }

        return service;
    }

})();