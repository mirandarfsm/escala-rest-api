(function(){
	'use strict';
	
	angular
		.module('Escalante')
		.directive('sidebar',sidebar);

	function sidebar(){
		return {
	        templateUrl:'app/header/sidebar/sidebar.directive.html',
	        restrict: 'E',
	        controller: SidebarController,
	        controllerAs: 'vm' 
	    };
	}

	function SidebarController($scope,autenticacaoService){
		//$scope.isAuthenticated = AuthenticationService.isLogged()
	}

})();