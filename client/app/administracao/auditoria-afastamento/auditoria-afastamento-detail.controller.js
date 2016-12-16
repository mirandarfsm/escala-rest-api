(function() {
	'use strict';

	angular
		.module('Escalante')
		.controller('AuditoriaAfastamentoDetailController',AuditoriaAfastamentoDetailController);

	AuditoriaAfastamentoDetailController.$inject = ['afastamentoGetOne','$location'];

	function AuditoriaAfastamentoDetailController(afastamentoGetOne, $location) {
		var vm = this;

		vm.afastamento = afastamentoGetOne;

		vm.aceitar = aceitar;
		vm.rejeitar = rejeitar;

		function aceitar(){
			vm.afastamento.ativo = true;
			salvar();
		}
		
		function rejeitar(){
			vm.afastamento.ativo = false;
			salvar();
		}
		
		function salvar() {
			vm.afastamento.data_inicio = new Date(vm.afastamento.data_inicio)
			vm.afastamento.data_fim = new Date(vm.afastamento.data_fim)
			vm.afastamento.save().then(function() {
				$location.path("/auditoria-afastamento");
			});
		}
	}

})();