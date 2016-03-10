( function(){
	'use strict';

	angular
      .module("Escalante")
      .config(config);

	config.$inject = ['$routeProvider'];

	function config($routeProvider) {
		$routeProvider
		// cadastro de escala
		.when('/cadastro-escala', {
		  templateUrl: 'app/administracao/cadastro-escala/cadastro-escala-list.html',
		  controller: 'CadastroEscalaController',
		  controllerAs: 'vm',
		  resolve:{
		  	escalaGetList: escalaGetList
		  }
		})
		.when('/cadastro-escala/new', {
		  templateUrl: 'app/administracao/cadastro-escala/cadastro-escala-form.html',
		  controller: 'CadastroEscalaDetailController',
		  controllerAs: 'vm',
		  resolve:{
			escalaGetOne:escalaGetOne,
		  	usuarioGetList:usuarioGetList
		  }
		})
		.when('/cadastro-escala/:id', {
		  templateUrl: 'app/administracao/cadastro-escala/cadastro-escala-form.html',
		  controller: 'CadastroEscalaDetailController',
		  controllerAs: 'vm',
		  resolve:{
		  	escalaGetOne:escalaGetOne,
		  	usuarioGetList:usuarioGetList
		  }
		});
	}

	function escalaGetList(escalaService){
        return escalaService.getList();
    }

    function usuarioGetList(usuarioService){
    	return usuarioService.getList();
    }

    function escalaGetOne(escalaService,$route){
    	return escalaService.one($route.current.params.id);
    }

})();