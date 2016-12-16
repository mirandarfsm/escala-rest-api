(function(){
	'use strict';

	angular
		.module('Escalante')
		.factory('usuarioService',usuarioService);

	usuarioService.$inject = ['Restangular'];

	function usuarioService(Restangular){
		return Restangular.service('usuarios');
	}

})();