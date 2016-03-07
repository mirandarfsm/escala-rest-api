(function() {
	'use strict';

	angular
		.module('Escalante')
		.controller('AuditoriaAfastamentoDetailController',AuditoriaAfastamentoDetailController);

	AuditoriaAfastamentoDetailController.$inject = ['afastamentoGetOne','$location','afastamentoService'];

	function AuditoriaAfastamentoDetailController(afastamentoGetOne, $location,afastamentoService) {
		var vm = this;

		vm.afastamento = afastamentoGetOne;

		vm.salvar = salvar;

		function salvar() {
			vm.afastamento.data_inicio = new Date(self.data_inicio).getTime();
			vm.afastamento.data_fim = new Date(self.data_fim).getTime();
			afastamentoService.put(vm.afastamento).success(function() {
				$location.path("/gerencia-afastamento");
			});
		}
	}

})();