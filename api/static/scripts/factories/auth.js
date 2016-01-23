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
    return $http.get('/auth/request-token', {headers : headers})
      .success(function(data){
        usuario = data.usuario;
        usuario.token = data.token;
        $rootScope.usuario = usuario;
        return usuario;
      }).error(function(error){
        console.log('Error Login');
      });
  };

  service.logout = function(){
    usuario = undefined;
    $rootScope.usuario = undefined; 
  }

  service.isLogged = function(){
    return !!usuario;
  };

  return service;
});