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
			templateUrl: 'app/administracao/cadastro-usuario/cadastro-usuario-list.html',
			controller: 'CadastroUsuarioController',
			controllerAs: 'vm',
			resolve: {
				usuarioGetList: usuarioGetList
			}
		})
		.when('/cadastro-usuario/new', {
			templateUrl: 'app/administracao/cadastro-usuario/cadastro-usuario-form.html',
			controller: 'CadastroUsuarioDetailController',
			controllerAs: 'vm',
			resolve: {
				usuarioGetOne: usuarioGetOne
			}
		})
		.when('/cadastro-usuario/:id', {
			templateUrl: 'app/administracao/cadastro-usuario/cadastro-usuario-form.html',
			controller: 'CadastroUsuarioDetailController',
			controllerAs: 'vm',
			resolve: {
				usuarioGetOne: usuarioGetOne
			}
		});

        function usuarioGetList(usuarioService) {
            return usuarioService.getList();
        }

        function usuarioGetOne(usuarioService,$routeParams){
        	return usuarioService.one($routeParams.id);
        }
	}

})();