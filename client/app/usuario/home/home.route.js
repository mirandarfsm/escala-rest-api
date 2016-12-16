(function() {
  'use strict';

  angular
      .module("Escalante")
      .config(config);
  
  config.$inject = ['$routeProvider'];
  
  function config($routeProvider) {
	  
	  $routeProvider
	  .when("/", {
		  templateUrl: 'app/usuario/home/home.html',
		  controller: 'HomeController',
		  controllerAs: 'vm',
          resolve: {
		    	servicoGetList: servicoGetList,
                afastamentoGetList: afastamentoGetList
		    }
		});
  }
  
  function servicoGetList(autenticacaoService){
      return autenticacaoService.get().getList('servicos');
  }
  
  function afastamentoGetList(autenticacaoService) {
        return autenticacaoService.get().getList('afastamentos');
  }
    
})();