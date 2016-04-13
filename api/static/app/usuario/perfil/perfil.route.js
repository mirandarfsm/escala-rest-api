(function(){
	'use strict';
	
	angular
		.module('Escalante')
		.config(config);
	
	function config($routeProvider){
		$routeProvider 
		.when('/perfil-usuario', {
		    templateUrl: 'app/usuario/perfil/perfil.html',
		    controller: 'PerfilUsuarioController',
		    controllerAs: 'vm'
		});
	}
})();