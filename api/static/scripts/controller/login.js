app.controller('LoginCtrl',function($rootScope, $scope, $http, $location,$window) {
  var self = this;
  $scope.message = '';
  $scope.login = function() {
    delete $window.sessionStorage.token;
    var username = self.username;
    var password = self.password;
    var headers = username ? {Authorization: "Basic " + btoa(username + ":" + password)} : {};
    $http.get('/auth/request-token', {headers : headers})
      .success(function(data, status, headers, config) {
        $window.sessionStorage.usuario = JSON.stringify(data.usuario);
        $window.sessionStorage.token = 'Basic ' + btoa(data.token + ':');
        $scope.message = 'Welcome';
        $scope.isAuthenticated = true;
        //$rootScope.authenticated = true;
        $location.path("/");
      })
      .error(function(data, status, headers, config) {
        //$rootScope.authenticated = false;
        $scope.isAuthenticated = false;
        delete $window.sessionStorage.token;
        // Handle login errors here
        $scope.message = 'Error: Invalid user or password';
        $location.path("/login");
      });
  };
});