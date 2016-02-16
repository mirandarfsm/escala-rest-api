app.controller('LoginCtrl',function($scope,$location,AuthenticationService) {
  var self = this;
  $scope.login = function() {
    var username = self.username;
    var password = self.password;
    
    AuthenticationService.login(username,password)
      .success(function(){
        $location.path('/');
    });
  };
});