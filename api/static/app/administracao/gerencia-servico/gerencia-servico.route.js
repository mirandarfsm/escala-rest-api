(function(){
	'use strict';

	angular
		.module('Escalante')
		.config(config);
	
	config.$inject = ['$routeProvider'];
	
	function config($routeProvider){
		$routeProvider
		.when('/gerencia-servico',{
			templateUrl: 'app/administracao/gerencia-servico/gerencia-servico-list.html',
			controller: 'GerenciaServicoController',
			controllerAs: 'vm',
			resolve: {
				escalaGetList: escalaGetList
			}
		})
		.when('/gerencia-servico/escala/:id',{
			templateUrl: 'app/administracao/gerencia-servico/gerencia-servico-detail.html',
			controller: 'GerenciaServicoDetailController',
			controllerAs: 'vm',
			resolve: {
				
			}
		});
	}
	
	function escalaGetList(escalaService){
		return escalaService.getList();
    }
	
	function servicoGetList(escalaService,$route){
		return escalaService.one($route.params.id).getList('servico');
	}
    
	
})();