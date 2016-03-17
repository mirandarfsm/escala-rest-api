(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoDetailController',GerenciaServicoDetailController);
	
	GerenciaServicoDetailController.$inject = ['servicoGetList','$location'];
	
	function GerenciaServicoDetailController(servicoGetOne,$location){
		var vm = this;
		
		vm.servico = servicoGetOne;

		vm.salvar = salvar;


		function salvar() {
            vm.servico.save().then(function(){
                $location.path('/gerencia-servico');
            });
            //usuarioService.save(vm.usuario).success(function(){
            //});
        }
	}
	
})();