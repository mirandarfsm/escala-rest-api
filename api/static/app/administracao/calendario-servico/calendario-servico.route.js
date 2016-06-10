(function(){
	'use strict';

	angular
		.module('Escalante')
		.config(config);
	
	config.$inject = ['$routeProvider'];
	
	function config($routeProvider){
		$routeProvider
		.when('/calendario-servico',{
			templateUrl: 'app/administracao/calendario-servico/calendario-servico.html',
			controller: 'CalendarioServicoController',
			controllerAs: 'vm',
			resolve: {
				servicoGetList: servicoGetList,
				afastamentoGetList: afastamentoGetList,
			}
		});
	}
	function servicoGetList(servicoService){
		return servicoService.getList();
	}
	
	function afastamentoGetList(afastamentoService){
		return afastamentoService.getList();
	}
	
})();