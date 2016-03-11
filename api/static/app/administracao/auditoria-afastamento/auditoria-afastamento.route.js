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
		    templateUrl: 'app/administracao/auditoria-afastamento/auditoria-afastamento-list.html',
		    controller: 'AuditoriaAfastamentoController',
		    controllerAs: 'vm',
		    resolve:{
		    	afastamentoGetList:afastamentoGetList
		    }
		  })
		  .when('/auditoria-afastamento/:id', {
		    templateUrl: 'app/administracao/auditoria-afastamento/auditoria-afastamento-form.html',
		    controller: 'AuditoriaAfastamentoDetailController',
		    controllerAs: 'vm',
		    resolve: {
		    	afastamentoGetOne:afastamentoGetOne
		    }
		  });

        function afastamentoGetList(afastamentoService) {
            return afastamentoService.getList();
        }

        function afastamentoGetOne(afastamentoService,$route){
        	var id = $route.current.params.id;
	    	if(id)
	    		return afastamentoService.one(id).get();
	    	return afastamentoService.one();
        }
	}

})();