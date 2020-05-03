(function() {
    'use strict';

    angular
        .module('Escalante')
        .controller('ErrorController', ErrorController);

    ErrorController.$inject = ['$location', 'error404'];

    function ErrorController($location, error404) {
        var vm = this;

        vm.error404 = error404

    }
})();