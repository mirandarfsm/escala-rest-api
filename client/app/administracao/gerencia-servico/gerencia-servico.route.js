(function() {
    'use strict';

    angular
        .module('Escalante')
        .config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        $routeProvider
            .when('/gerencia-servico', {
                templateUrl: 'app/administracao/gerencia-servico/gerencia-servico.html',
                controller: 'GerenciaServicoController',
                controllerAs: 'vm',
                resolve: {
                    escalaGetList: escalaGetList,
                    servicoGetList: servicoGetList
                }
            })
            .when('/cadastro-servico/new', {
                templateUrl: 'app/administracao/gerencia-servico/cadastro-servico-detail.html',
                controller: 'CadastroServicoDetailController',
                controllerAs: 'vm',
                resolve: {
                    servicoGetOne: servicoGetOne,
                    escalaGetList: escalaGetList
                }
            })
            .when('/gerencia-servico/:id', {
                templateUrl: 'app/administracao/gerencia-servico/gerencia-servico-detail.html',
                controller: 'GerenciaServicoDetailController',
                controllerAs: 'vm',
                resolve: {
                    servicoGetOne: servicoGetOne
                }
            });
    }

    function escalaGetList(escalaService) {
        return escalaService.getList();
    }

    function servicoGetList(servicoService) {
        return servicoService.getList();
    }

    function servicoGetOne(servicoService, $route) {
        var id = $route.current.params.id;
        if (id) {
            return servicoService.one(id).get();
        }
        return servicoService.one();
    }


})();