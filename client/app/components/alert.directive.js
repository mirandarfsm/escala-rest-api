(function() {
    'use strict';

    angular
        .module('Escalante')
        .directive('alert', alert);

    function alert() {
        var directive = {
            template: `
                <div uib-alert ng-repeat="alert in vm.alerts" ng-class="'alert-' + (alert.type || 'warning')" dismiss-on-timeout="{{alert.timeout}}" close="vm.closeAlert($index)">
                    {{alert.msg}}
                </div>`,
            restrict: 'EA',
            scope: {},
            controller: AlertController,
            controllerAs: 'vm',
            bindToController: true
        };

        return directive;
    }

    AlertController.$inject = ['alertService'];

    function AlertController(alertService) {
        var vm = this;
        vm.alerts = alertService.getAlerts();

        vm.closeAlert = closeAlert;

        function closeAlert(index) {
            alertService.closeByIndex(index)
        }
    }

})();