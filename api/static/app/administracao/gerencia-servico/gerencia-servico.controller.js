(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoController',GerenciaServicoController);
	
	GerenciaServicoController.$inject = ['escalaGetList','escalaService','$location'];
	
	function GerenciaServicoController(escalaGetList,escalaService,$location){
		var vm = this;
		
		vm.escalas = escalaGetList;
		
		vm.gerarEscala = gerarEscala; 
		vm.cancelar = cancelar;
		
	    function gerarEscala(){
	        escalaService.one(vm.escala.id).one('generate').then(function(){
	        	$location.path('/gerencia-servico/escala/'+vm.escala.id);
	        });
	    }
	    
	    function cancelar (){
	        vm.escala = {}
	        vm.data_inicio = "";
	        vm.data_fim = undefined;
	    }
	}
	
})();