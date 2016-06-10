(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoController',GerenciaServicoController)
		.controller('TrocaServicoModalController',GerenciaServicoController);
	
	GerenciaServicoController.$inject = ['escalaGetList','servicoGetList','$uibModal'];
	
	function GerenciaServicoController(escalaGetList,servicoGetList,$uibModal){
		var vm = this;

		vm.tipos = ['Preto','Vermelho','Roxo'];
		vm.escalas = escalaGetList;
		vm.servicos = servicoGetList;
		
		vm.getServicos = getServicos;
		
		function getServicos(){
			vm.servicos = vm.escala.getList('servico').$object
		}
		
	}
})();