(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('CadastroAfastamentoDetailController',CadastroAfastamentoDetailController); 
	
	CadastroAfastamentoDetailController.$inject = ['afastamentoGetOne','$location'];
	
	function CadastroAfastamentoDetailController(afastamentoGetOne,$location){
	    var vm = this;
	    
	    vm.afastamento = afastamentoGetOne;
	    
	    vm.salvar = salvar;
	    
	    function salvar(){
	        vm.afastamento.data_inicio = new Date(vm.data_inicio).getTime();
	    	vm.afastamento.data_fim = new Date(vm.data_fim).getTime();
			vm.afastamento.save().then(function(){
	            $location.path("/cadastro-afastamento");
	    	});	
		}
	}
	
})();