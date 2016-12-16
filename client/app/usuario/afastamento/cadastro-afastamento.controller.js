(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('CadastroAfastamentoController',CadastroAfastamentoController); 
	
	CadastroAfastamentoController.$inject = ['afastamentoGetList'];
	
	function CadastroAfastamentoController(afastamentoGetList){
	    var vm = this;
	    
	    vm.afastamentos = afastamentoGetList;
	    
	    vm.deletar = deletar;
	
		function deletar(index){
			var afastamento = vm.afastamentos[index];
	        afastamento.remove().then(function(data){
	            vm.afastamentos.splice(index,1);
	        });
		}

	}
	
})();