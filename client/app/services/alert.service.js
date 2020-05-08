(function() {
    'use strict';

    angular
        .module('Escalante')
        .factory('alertService', alertService);

    alertService.$inject = ['$rootScope'];

    function alertService($rootScope) {

        $rootScope.alerts = [];

        let id = 0;

        var service = {
            add: add,
            addError: addError,
            addSuccess: addSuccess,
            getAlerts: getAlerts,
            close: close,
            closeByIndex: closeByIndex
        };

        function add(type, msg, params, timeout) {
            $rootScope.alerts.push({ id: id, type: type, msg: msg, params: params, timeout: timeout });
            id++;
        }

        function addSuccess(msg, params) {
            add('success', msg, params, 5000);
        }

        function addError(msg, params) {
            add('danger', msg, params, 5000);
        }

        function getAlerts() {
            return $rootScope.alerts;
        }

        function close(id) {
            $rootScope.alerts = $rootScope.alerts.filter(alert => alert.id !== id);
        }

        function closeByIndex(index) {
            $rootScope.alerts.splice(index, 1);
        }

        return service;
    }

})();