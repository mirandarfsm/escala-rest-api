(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoDetailController',GerenciaServicoDetailController);
	
	GerenciaServicoDetailController.$inject = ['servicoGetList','escalaService','$scope'];
	
	function GerenciaServicoDetailController(servicoGetList,escalaService,$scope){
		var vm = this;
		
		vm.itemPerPage = 10;
		vm.itemsPerPage = [10, 30, 50];
		vm.servicos = servicoGetList;
		vm.tipos = ['Preto','Vermelho','Roxo'];
		
		
		vm.pageChanged = pageChanged;
		
		function pageChanged(){
			vm.servicos = vm.servicos.getList({
				per_page: itemPerPage, 
				page: vm.servicos.meta.page}).$object;
		}
	}
	
})();