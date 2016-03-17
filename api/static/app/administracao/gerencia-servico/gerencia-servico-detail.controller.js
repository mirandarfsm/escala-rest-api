(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoDetailController',GerenciaServicoDetailController);
	
	GerenciaServicoDetailController.$inject = ['servicoGetOne','escalaService','$location'];
	
	function GerenciaServicoDetailController(servicoGetOne,escalaService,$location){
		var vm = this;
		
		vm.servico = servicoGetOne;
		
		vm.usuarios = getUsuarioList();
		
		vm.salvar = salvar;
		
		
		function getUsuarioList(){
			return escalaService.one(vm.servico.escala.id).one('usuario').getList().$object;
		}

		function salvar() {
            vm.servico.save().then(function(){
                $location.path('/gerencia-servico');
            });
        }
	}
	
})();