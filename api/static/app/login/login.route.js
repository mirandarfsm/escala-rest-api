( function(){
	'use strict';

	angular
      .module("Escalante")
      .config(config);

	config.$inject = ['$routeProvider'];

	function config($routeProvider) {
		$routeProvider
		// login
		.when('/login',{
			templateUrl: 'app/login/login.html',
			controller: 'LoginController',
			controllerAs: 'vm'
		});
	}

})();