(function(){
	'use strict';

	angular
		.module('Escalante')
		.config(config); 
	
	config.$inject = ['$routeProvider'];
				
	function config($routeProvider){
		$routeProvider
		.when('/cadastro-afastamento', {
		    templateUrl: 'cadastro-afastamento-list.html',
		    controller: 'CadastroAfastamentoController',
		    controllerAs: 'vm',
		    resolve: {
		    	afastamentoGetList: afastamentoGetList
		    }
		  })
		  .when('/cadastro-afastamento/new', {
		    templateUrl: 'cadastro-afastamento-form.html',
		    controller: 'CadastroAfastamentoNewController',
		    controllerAs: 'vm',
		    resolve: {
		    	afastamentoGetOne: undefined
		    }
		  })
		  .when('/cadastro-afastamento/:id', {
		    templateUrl: 'cadastro-afastamento-form.html',
		    controller: 'CadastroAfastamentoDetailController',
		    controllerAs: 'vm',
		    resolve:{
		    	afastamentoGetOne: afastamentoGetOne
		    }
		  });
	}
	
	function afastamentoGetList(autenticacaoService) {
        return usuarioService.one(USER_LOGGED).getList('afastamentos');
    }

    function afastamentoGetOne(autenticacaoService,$routeParams){
    	return usuarioService.one(USER_LOGGED).one('afastamentos',$routeParams.id);
    }
})();