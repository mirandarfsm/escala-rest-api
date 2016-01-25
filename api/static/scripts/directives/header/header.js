app.directive("header",function(){
	return {
        templateUrl:'scripts/directives/header/header.html',
        restrict: 'E',
        controller: 'HeaderCtrl'
    	};
});

app.controller('HeaderCtrl',function($scope,$location,$rootScope,AuthenticationService){
	$scope.logout = function () {
		AuthenticationService.logout();
	    $location.path({redirectTo: "/login"});
  	};
});