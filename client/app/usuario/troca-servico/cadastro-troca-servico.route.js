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
		templateUrl: 'app/usuario/troca-servico/cadastro-troca-servico.html',
		controller: 'CadastroTrocaServicoController',
		controllerAs: 'vm',
		resolve: {
			trocaServicoGetList:trocaServicoGetList,
			trocaServicoPendenteGetList:trocaServicoPendenteGetList
		}
	})
	.when('/cadastro-troca-servico/new', {
		templateUrl: 'app/usuario/troca-servico/cadastro-troca-servico-detail.html',
		controller: 'CadastroTrocaServicoDetailController',
		controllerAs: 'vm',
		resolve: {
			servicoGetList: servicoGetList,
			trocaServicoGetOne: trocaServicoGetOne
		}
	});

	function trocaServicoGetList(autenticacaoService){
		return autenticacaoService.get().getList('troca-servico');
	}

	function trocaServicoPendenteGetList(autenticacaoService){
		return autenticacaoService.get().one('troca-servico').getList('pendentes');
	}

	function servicoGetList(autenticacaoService){
		return autenticacaoService.get().getList('servicos');
	}

	function trocaServicoGetOne(autenticacaoService,$route){
		var id = $route.current.params.id;
    	if(id)
    		return autenticacaoService.get().one('troca-servico',id).get();
    	return autenticacaoService.get().one('troca-servico');

	}


  }
    

})();