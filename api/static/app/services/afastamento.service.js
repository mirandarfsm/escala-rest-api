(function(){
	'use strict';

	angular
		.module('Escalante')
		.factory('afastamentoService',afastamentoService);

	escalaService.$inject = ['Restangular'];

	function afastamentoService(Restangular){
		return Restangular.service('afastamento');
	}

})();