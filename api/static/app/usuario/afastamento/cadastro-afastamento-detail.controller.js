(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('CadastroAfastamentoDetailController',CadastroAfastamentoDetailController); 
	
	CadastroAfastamentoDetailController.$inject = ['afastamentoGetOne','$location','$rootScope'];
	
	function CadastroAfastamentoDetailController(afastamentoGetOne,$location,$rootScope){
	    var vm = this;
	    
	    vm.afastamento = afastamentoGetOne;
		console.log(vm.afastamento)
		vm.popupDataInicio = false;
	    vm.popupDataFim = false;
		
        vm.openDataInicio = openDataInicio;
		vm.openDataFim = openDataFim;
	    vm.salvar = salvar;
   
		
        function openDataInicio(){
            vm.popupDataInicio = true;
        }
   
        function openDataFim(){
            vm.popupDataFim = true;
        }
	    
	    function salvar(){
			vm.afastamento.save().then(function(){
	            $location.path("/cadastro-afastamento");
	    	});	
		}
	}
	
})();