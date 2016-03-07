(function(){
	'use strict';
	
	angular
		.module('Escalante')
		.config(config);
	
	function config($routeProvider){
		$routeProvider 
		.when('/perfil-usuario', {
		    templateUrl: 'perfil-usuario-form.html',
		    controller: 'PerfilUsuarioController',
		    controllerAs: 'vm'
		});
	}
});