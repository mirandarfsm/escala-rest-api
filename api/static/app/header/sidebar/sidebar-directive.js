(function(){
	'use strict';
	
	angular
		.module('Escalante')
		.directive('sidebar',sidebar);

	function sidebar(){
		return {
	        templateUrl:'sidebar-directive.html',
	        restrict: 'E',
	        controller: SidebarController,
	        controllerAs: 'vm' 
	    };
	}

	function SidebarController($scope,AuthenticationService){
		//$scope.isAuthenticated = AuthenticationService.isLogged()
	}

})();