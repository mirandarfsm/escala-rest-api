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
		  templateUrl: 'app/administracao/cadastro-escala/cadastro-escala.html',
		  controller: 'CadastroEscalaController',
		  controllerAs: 'vm',
		  resolve:{
		  	escalaGetList: escalaGetList
		  }
		})
		.when('/cadastro-escala/new', {
		  templateUrl: 'app/administracao/cadastro-escala/cadastro-escala-detail.html',
		  controller: 'CadastroEscalaDetailController',
		  controllerAs: 'vm',
		  resolve:{
			escalaGetOne:escalaGetOne,
		  	usuarioGetList:usuarioGetList
		  }
		})
		.when('/cadastro-escala/:id', {
		  templateUrl: 'app/administracao/cadastro-escala/cadastro-escala-detail.html',
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
    	var id = $route.current.params.id;
    	if(id)
    		return escalaService.one(id).get();
    	return escalaService.one();
    }

})();