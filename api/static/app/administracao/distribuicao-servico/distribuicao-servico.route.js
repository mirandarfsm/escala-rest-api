(function(){
	'use strict';

	angular
		.module('Escalante')
		.config(config);
	
	config.$inject = ['$routeProvider'];
	
	function config($routeProvider){
		$routeProvider
		.when('/distribuicao-servico',{
			templateUrl: 'app/administracao/distribuicao-servico/distribuicao-servico.html',
			controller: 'DistribuicaoServicoController',
			controllerAs: 'vm',
			resolve: {
				escalaGetList: escalaGetList
			}
		});
	}
	
	function escalaGetList(escalaService){
		return escalaService.getList();
    }
    
})();