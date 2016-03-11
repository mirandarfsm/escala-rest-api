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
			}
		});
	}
	
})();