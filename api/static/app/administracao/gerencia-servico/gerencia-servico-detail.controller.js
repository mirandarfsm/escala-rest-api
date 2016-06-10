(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoDetailController',GerenciaServicoDetailController);
	
	GerenciaServicoDetailController.$inject = ['servicoGetOne','escalaService','$location'];
	
	function GerenciaServicoDetailController(servicoGetOne,escalaService,$location){
		var vm = this;
		
		vm.servico = servicoGetOne;
		escalaService.one(vm.servico.usuario_escala.escala.id).getList('usuario-escala').then(function(data){
			vm.listUsuarioEscala = data;
			console.log(vm.listUsuarioEscala[0]);
		});
		
		vm.salvar = salvar;
		
		
		function getUsuarioEscalaList(){
			return escalaService.one(vm.servico.usuario_escala.escala.id).getList('usuario-escala');
		}

		function salvar() {
			vm.servico.usuario_escala = vm.substituto;
			vm.servico.data = new Date(vm.servico.data);
            vm.servico.save().then(function(){
                $location.path('/gerencia-servico');
            });
        }
		
	}
	
})();