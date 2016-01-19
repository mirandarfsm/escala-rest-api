app.directive("header",function(){
	return {
        templateUrl:'scripts/directives/header/header.html',
        restrict: 'E',
        controller: 'HeaderCtrl as headerCtrl'
    	};
});

app.controller('HeaderCtrl',function($scope,$window,$location,$rootScope){
	$scope.isAuthenticated = function(){
		return $window.sessionStorage.token;
	};
	
	//$scope.usuario = JSON.parse($window.sessionStorage.usuario); 
	$scope.logout = function () {
	    $scope.welcome = '';
	    $scope.message = '';
	    $scope.isAuthenticated = false;
	    //$rootScope.authenticated = false;
	    delete $window.sessionStorage.token;
	    $location.path({redirectTo: "/login"});
  	};
});