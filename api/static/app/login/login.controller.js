(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('LoginController',LoginController);
	
	LoginController.$inject = ['$location','autenticacaoService'];
	
	function LoginController($location,autenticacaoService) {
	  var vm = this;
	  
	  vm.login = login;
	  	  
	  function login() {
		  autenticacaoService.login(vm.username,vm.password).success(function(){
	        $location.path('/');
	    }).error(function(error){
	    	console.log(error);
	    });
	  }
	}
})();