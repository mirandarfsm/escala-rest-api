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
        $timeout(service.logout, 3600000);
        return usuario;
      });
  };

  service.logout = function(){
    usuario = undefined;
    $rootScope.usuario = undefined; 
  }

  service.isLogged = function(){
    return !!usuario;
  };

  service.isAdmin = function(){
    if(service.isLogged()){
      return usuario.admin;
    }
    return false;
  };

  return service;
});