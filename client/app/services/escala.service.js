(function(){
	'use strict';

	angular
		.module('Escalante')
		.factory('escalaService',escalaService);

	escalaService.$inject = ['Restangular'];

	function escalaService(Restangular){
		return Restangular.service('escalas');
	}

})();