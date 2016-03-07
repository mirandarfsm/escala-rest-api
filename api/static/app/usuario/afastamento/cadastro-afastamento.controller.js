(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('CadastroAfastamentoController',CadastroAfastamentoController); 
	
	CadastroAfastamentoController.$inject = ['USER_LOGGED','afastamentoGetList','usuarioService'];
	
	function CadastroAfastamentoController(USER_LOGGED,afastamentoGetList,usuarioService){
	    var vm = this;
	    
	    vm.afastamentos = afastamentoGetList.objects;
	    
	    vm.deletar = deletar;
	
		function deletar(index){
			var afastamento = vm.afastamentos[index];
	        usuarioService.one(USER_LOGGED).one('afastamento',afastamento.id).remove().then(function(data){
	            self.afastamentos.splice(index,1);
	        });
		}

	}
	
})();