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
	
	function afastamentoGetList(usuarioService,USER_LOGGED) {
        return usuarioService.one(USER_LOGGED).getList('afastamentos');
    }

    function afastamentoGetOne(usuarioService,USER_LOGGED,$routeParams){
    	return usuarioService.one(USER_LOGGED).one('afastamentos',$routeParams.id);
    }
})();