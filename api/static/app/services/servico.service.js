(function(){
	'use strict';

	angular
		.module('Escalante')
		.factory('servicoService',servicoService);

	servicoService.$inject = ['Restangular'];

	function servicoService(Restangular){
		return Restangular.service('servicos');
	}

})();