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
		  templateUrl: 'cadastro-escala-list.html',
		  controller: 'CadastroEscalaController',
		  controllerAs: 'vm',
		  resolve:{
		  	escalaGetList: escalaGetList
		  }
		})
		.when('/cadastro-escala/new', {
		  templateUrl: 'cadastro-escala-form.html',
		  controller: 'CadastroEscalaDetailController',
		  controllerAs: 'vm',
		  resolve:{
		  	escalaGetOne:undefined,
		  	usuarioGetList:usuarioGetList
		  }
		})
		.when('/cadastro-escala/:id', {
		  templateUrl: 'cadastro-escala-form.html',
		  controller: 'CadastroEscalaDetailCtrl',
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

    function escalaGetOne(escalaService,$routeParams){
    	return escalaService.one($routeParams.id);
    }

})();