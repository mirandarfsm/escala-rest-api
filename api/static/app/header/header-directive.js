(function() {
	'use strict';
	
	angular
		.module()
		.directive('header',header);
	
	function header(){
		return {
	        templateUrl:'header.directive.html',
	        restrict: 'E',
	        controller: HeaderController,
	        controllerAs: 'vm',
	        bindToController: true
	    };
	}
});

);

function HeaderController($scope,$location,$rootScope,AuthenticationService){
	var vm = this;
	
	vm.logout = logout;
	
	function logout() {
		AuthenticationService.logout();
	    $location.path({redirectTo: "/login"});
  	}
}