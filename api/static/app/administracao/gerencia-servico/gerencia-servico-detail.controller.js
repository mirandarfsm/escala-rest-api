(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoDetailController',GerenciaServicoDetailController);
	
	GerenciaServicoDetailController.$inject = ['servicoGetList'];
	
	function GerenciaServicoDetailController(servicoGetList){
		var vm = this;
		
		vm.servicos = servicoGetList;
		vm.tipos = ['Preto','Vermelho','Roxo'];
	}
	
})();