
/*app.factory('authInterceptor', function ($rootScope, $q, $window) {
  return {
    request: function (config) {
      config.headers = config.headers || {};
      if ($window.sessionStorage.token) {
        config.headers.Authorization = $window.sessionStorage.token;
      }
      return config;
    },
    responseError: function (rejection) {
      if (rejection.status === 401) {
        // handle the case where the user is not authenticated
      }
      return $q.reject(rejection);
    }
  };
});

app.config(function ($httpProvider) {
  $httpProvider.interceptors.push('authInterceptor');
});
*/
app.factory('AuthenticationService', function ($http, $rootScope, $timeout) {
  var usuario = undefined;
  
  var service = {};

  service.getUsuario = function(){
    return usuario;
  };

  service.getToken = function(){
    return usuario.token;
  };
  
  service.login = function (username, password) {

    var headers = {Authorization: "Basic " + btoa(username + ":" + password)};
    $http.get('/auth/request-token', {headers : headers})
      .success(function(data){
        usuario = data.usuario;
        usuario.token = data.token;
        $rootScope.usuario = usuario;
        return usuario;
      });
  };

  service.logout = function(){
    usuario = undefined;
    $rootScope.usuario = undefined; 
  }

  service.isLogged = function(){
    return usuario;
  };

  return service;
});