(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('LoginController',LoginController
				
	function LoginController($scope,$location,AuthenticationService) {
	  var vm = this;
	  
	  vm.login = login;
	  
	  function login() {
	    AuthenticationService.login(vm.username,vm.password).success(function(){
	        $location.path('/');
	    }).error(function(error){
	    	console.log(error);
	    });
	  }
	}
})();