(function() {
  'use strict';

  angular
      .module("Escalante")
      .config(config);
  
  config.$inject = ['$routeProvider'];
  
  function config($routeProvider) {
	  
	  $routeProvider
	  .when("/", {
		  templateUrl: 'app/usuario/home/teste.html',
		  controller: 'TesteController',
		  controllerAs: 'vm'
		});
  }
    
})();