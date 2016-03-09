(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('CadastroAfastamentoDetailController',CadastroAfastamentoDetailController); 
	
	CadastroAfastamentoDetailController.$inject = ['USER_LOGGED','afastamentoGetOne','usuarioService','$location'];
	
	function CadastroAfastamentoDetailController(USER_LOGGED,afastamentoGetOne,usuarioService,$location){
	    var vm = this;
	    
	    vm.afastamento = afastamentoGetOne;
	    
	    vm.salvar = salvar;
	    
	    function salvar(){
	        vm.afastamento.data_inicio = new Date(vm.data_inicio).getTime();
	    	vm.afastamento.data_fim = new Date(vm.data_fim).getTime();
			usuarioService.one(USER_LOGGED).one('afastamentos',vm.afastamento.id).save().success(function(){
	            $location.path("/cadastro-afastamento");
	    	});	
		}
	}
	
})();