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

  HeaderController.$inject = ['$scope','$location','autenticacaoService'];

	function HeaderController($scope,$location,autenticacaoService){
		var vm = this;

		$scope.logout = logout;

		function logout() {
			autenticacaoService.logout();
		    $location.path({redirectTo: "/login"});
	  	}
	}

})();
