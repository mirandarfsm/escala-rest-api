(function(){
	'use strict';

	angular
		.module('Escalante')
		.factory('usuarioService',usuarioService);

	escalaService.$inject = ['Restangular'];

	function usuarioService(Restangular){
		return Restangular.service('usuarios');
	}

})();