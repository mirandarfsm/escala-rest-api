( function(){
    'use strict';

    angular 
        .module('Escalante')
        .controller('AuditoriaAfastamentoController',AuditoriaAfastamentoController);

    AuditoriaAfastamentoController.$inject = ['afastamentoGetList','$location'];
         
    function AuditoriaAfastamentoController(afastamentoGetList,$location){
        var vm = this;
        
        vm.afastamentos = afastamentoGetList;
        vm.aceitar = aceitar;
		vm.rejeitar = rejeitar;

		function aceitar(afastamento){
			afastamento.ativo = true;
			salvar(afastamento);
		}
		
		function rejeitar(afastamento){
			afastamento.ativo = false;
			salvar(afastamento);
		}
		
		function salvar(afastamento) {
			afastamento.data_inicio = new Date(afastamento.data_inicio)
			afastamento.data_fim = new Date(afastamento.data_fim)
			afastamento.save().then(function() {
				$location.path("/auditoria-afastamento");
			});
		}
    }

})();