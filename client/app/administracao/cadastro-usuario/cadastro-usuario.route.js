( function(){
	'use strict';

	angular
      .module("Escalante")
      .config(config);

	config.$inject = ['$routeProvider'];

	function config($routeProvider) {
		$routeProvider
		// cadastro de usuario
		.when('/cadastro-usuario', {
			templateUrl: 'app/administracao/cadastro-usuario/cadastro-usuario.html',
			controller: 'CadastroUsuarioController',
			controllerAs: 'vm',
			resolve: {
				usuarioGetList: usuarioGetList
			}
		})
		.when('/cadastro-usuario/new', {
			templateUrl: 'app/administracao/cadastro-usuario/cadastro-usuario-detail.html',
			controller: 'CadastroUsuarioDetailController',
			controllerAs: 'vm',
			resolve: {
				usuarioGetOne: usuarioGetOne
			}
		})
		.when('/cadastro-usuario/:id', {
			templateUrl: 'app/administracao/cadastro-usuario/cadastro-usuario-detail.html',
			controller: 'CadastroUsuarioDetailController',
			controllerAs: 'vm',
			resolve: {
				usuarioGetOne: usuarioGetOne
			}
		});

        function usuarioGetList(usuarioService) {
            return usuarioService.getList();
        }

        function usuarioGetOne(usuarioService,$route){
        	var id = $route.current.params.id;
        	if(id)
        		return usuarioService.one(id).get();
        	return usuarioService.one();
        }
	}

})();