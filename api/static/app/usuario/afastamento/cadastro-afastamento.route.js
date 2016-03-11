(function(){
	'use strict';

	angular
		.module('Escalante')
		.config(config); 
	
	config.$inject = ['$routeProvider'];
				
	function config($routeProvider){
		$routeProvider
		.when('/cadastro-afastamento', {
		    templateUrl: 'app/usuario/afastamento/cadastro-afastamento-list.html',
		    controller: 'CadastroAfastamentoController',
		    controllerAs: 'vm',
		    resolve: {
		    	afastamentoGetList: afastamentoGetList
		    }
		  })
		  .when('/cadastro-afastamento/new', {
		    templateUrl: 'app/usuario/afastamento/cadastro-afastamento-form.html',
		    controller: 'CadastroAfastamentoDetailController',
		    controllerAs: 'vm',
		    resolve: {
		    	afastamentoGetOne: afastamentoGetOne
		    }
		  })
		  .when('/cadastro-afastamento/:id', {
		    templateUrl: 'app/usuario/afastamento/cadastro-afastamento-form.html',
		    controller: 'CadastroAfastamentoDetailController',
		    controllerAs: 'vm',
		    resolve:{
		    	afastamentoGetOne: afastamentoGetOne
		    }
		  });
	}
	
	function afastamentoGetList(autenticacaoService) {
        return autenticacaoService.get().getList('afastamentos');
    }

    function afastamentoGetOne(autenticacaoService,$route){
    	var id = $route.current.params.id;
    	if(id)
    		return autenticacaoService.get().one('afastamentos',id).get();
    	return autenticacaoService.get().one('afastamentos');
    }
})();