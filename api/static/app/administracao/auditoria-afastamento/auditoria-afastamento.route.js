( function(){
	'use strict';

	angular
      .module("Escalante")
      .config(config);

	config.$inject = ['$routeProvider'];

	function config($routeProvider) {
		$routeProvider
		// auditoria de Afastamento
		.when('/auditoria-afastamento', {
		    templateUrl: 'auditoria-afastamento-list.html',
		    controller: 'AuditoriaAfastamentoController',
		    controllerAs: 'vm',
		    resolve:{
		    	afastamentoGetList:afastamentoGetList
		    }
		  })
		  .when('/auditoria-afastamento/:id', {
		    templateUrl: 'auditoria-afastamento-form.html',
		    controller: 'AuditoriaAfastamentoDetailController',
		    controllerAs: 'vm',
		    resolve: {
		    	afastamentoGetOne:afastamentoGetOne
		    }
		  });

        function afastamentoGetList(afastamentoService) {
            return afastamentoService.getList();
        }

        function afastamentoGetOne(afastamentoService,$routeParams){
        	return afastamentoService.one($routeParams.id);
        }
	}

})();