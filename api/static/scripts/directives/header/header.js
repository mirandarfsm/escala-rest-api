app.directive("header",function(){
	return {
        templateUrl:'scripts/directives/header/header.html',
        restrict: 'E',
        controller: 'HeaderCtrl as headerCtrl'
    	};
});

app.controller('HeaderCtrl',function($scope,$location,$rootScope,AuthenticationService){
	/*
	$scope.isAuthenticated = function(){
		return $window.sessionStorage.token;
	};
	*/
	//$scope.usuario = JSON.parse($window.sessionStorage.usuario); 
	$scope.logout = function () {
		AuthenticationService.logout();
	    $location.path({redirectTo: "/login"});
  	};
});