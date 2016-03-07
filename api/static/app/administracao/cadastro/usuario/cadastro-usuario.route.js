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
			templateUrl: 'cadastro-usuario-list.html',
			controller: 'CadastroUsuarioCtrl',
			controllerAs: 'vm',
			resolve: {
				usuarioGetList: usuarioGetList
			}
		})
		.when('/cadastro-usuario/new', {
			templateUrl: 'cadastro-usuario-form.html',
			controller: 'CadastroUsuarioNewCtrl',
			controllerAs: 'vm',
			resolve: {
				usuarioGetOne: undefined
			}
		})
		.when('/cadastro-usuario/:id', {
			templateUrl: 'cadastro-usuario-form.html',
			controller: 'CadastroUsuarioDetailCtrl',
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