app.controller('LoginCtrl',function($rootScope, $scope, $http, $location,$window,AuthenticationService) {
  var self = this;
  $scope.message = '';
  $scope.login = function() {
    var username = self.username;
    var password = self.password;
    
    AuthenticationService.login(username,password)
      .success(function(){
        $location.path('/');
    }).error(function(error){
      console.log('401 Unauthorized!');  
    });
  };
});