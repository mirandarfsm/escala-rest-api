(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoController',GerenciaServicoController);
	
	GerenciaServicoController.$inject = ['escalaGetList','escalaService','$location'];
	
	function GerenciaServicoController(escalaGetList){
		var vm = this;
		
		vm.escalas = escalaGetList;
		vm.tipos = ['Preto','Vermelho','Roxo'];
		
		vm.getServicos = getServicos;
		vm.pageChanged = pageChanged;
		
		function pageChanged(){
			vm.servicos = vm.servicos.getList({
				per_page: vm.itemPerPage, 
				page: vm.servicos.meta.page}).$object;
		}

		function getServicos(){
			vm.servicos = vm.escala.getList('servico').$object;
		}

	}
	
})();