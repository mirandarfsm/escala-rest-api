(function(){
	'use strict';

	angular
		.module('Escalante')
		.factory('afastamentoService',afastamentoService);

	afastamentoService.$inject = ['Restangular'];

	function afastamentoService(Restangular){
		return Restangular.service('servicos');
	}

})();