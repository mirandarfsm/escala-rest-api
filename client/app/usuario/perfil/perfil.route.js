(function() {
    'use strict';

    angular
        .module('Escalante')
        .config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        $routeProvider
            .when('/perfil-usuario', {
                templateUrl: 'app/usuario/perfil/perfil.html',
                controller: 'PerfilUsuarioController',
                controllerAs: 'vm',
                resolve: {
                    passwordChangeOne: passwordChangeOne
                }
            });
    }

    function passwordChangeOne(autenticacaoService) {
        return autenticacaoService.get().one('change-password');
    }

})();