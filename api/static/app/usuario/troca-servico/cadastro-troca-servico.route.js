(function() {
  'use strict';

  angular
      .module("Escalante")
      .config(config);
  
  config.$inject = ['$routeProvider'];
  
  function config($routeProvider) {
	$routeProvider  
	// cadastro de troca de servico
	.when('/cadastro-troca-servico', {
		templateUrl: 'app/usuario/troca-servico/cadastro-troca-servico-list.html',
		controller: 'CadastroTrocaServicoController',
		controllerAs: 'vm',
		resolve: {
			trocaServicoGetList:trocaServicoGetList,
			trocaServicoPendenteGetList:trocaServicoPendenteGetList
		}
	})
	.when('/cadastro-troca-servico/new', {
		templateUrl: 'app/usuario/troca-servico/cadastro-troca-servico-form.html',
		controller: 'CadastroTrocaServicoDetailController',
		controllerAs: 'vm',
		resolve: {

		}
	});

	function trocaServicoGetList(autenticacaoService){
		return autenticacaoService.get().getList('troca-servico');
	}

	function trocaServicoPendenteGetList(autenticacaoService,$routeParams){
		return autenticacaoService.get().one('troca-servico',$routeParams.id);
	}

  }
    

})();