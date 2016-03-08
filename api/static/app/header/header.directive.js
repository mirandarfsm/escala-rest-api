(function() {
	'use strict';
	
	angular
		.module('Escalante')
		.directive('header',header);
	
	function header(){
		return {
	        templateUrl:'app/header/header.directive.html',
	        restrict: 'E',
	        controller: HeaderController,
	        controllerAs: 'vm',
	        bindToController: true
	    };
	}

	function HeaderController($scope,$location,$rootScope,autenticacaoService){
		var vm = this;
		
		vm.logout = logout;
		
		function logout() {
			autenticacaoService.logout();
		    $location.path({redirectTo: "/login"});
	  	}
	}

})();