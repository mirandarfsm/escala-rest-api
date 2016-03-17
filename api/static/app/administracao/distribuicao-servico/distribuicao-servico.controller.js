(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('DistribuicaoServicoController',DistribuicaoServicoController);
	
	DistribuicaoServicoController.$inject = ['escalaGetList'];
	
	function DistribuicaoServicoController(escalaGetList){
		var vm = this;
		
		vm.escalas = escalaGetList;
		
		vm.gerarEscala = gerarEscala; 
		
	    function gerarEscala(){
	        vm.escala.one('generate').put();
	    }
	}
	
})();