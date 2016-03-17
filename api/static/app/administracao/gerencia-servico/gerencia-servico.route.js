(function(){
	'use strict';

	angular
		.module('Escalante')
		.config(config);
	
	config.$inject = ['$routeProvider'];
	
	function config($routeProvider){
		$routeProvider
		.when('/gerencia-servico',{
			templateUrl: 'app/administracao/gerencia-servico/gerencia-servico.html',
			controller: 'GerenciaServicoController',
			controllerAs: 'vm',
			resolve: {
				escalaGetList: escalaGetList
			}
		})
		.when('/gerencia-servico/:id',{
			templateUrl: 'app/administracao/gerencia-servico/gerencia-servico-detail.html',
			controller: 'GerenciaServicoDetailController',
			controllerAs: 'vm',
			resolve: {
				servicoGetOne: servicoGetOne
			}
		});
	}
	
	function escalaGetList(escalaService){
		return escalaService.getList();
    }
	
	function servicoGetOne(servicoService,$route){
		return servicoService.one($route.current.params.id).get();
	}
    
	
})();