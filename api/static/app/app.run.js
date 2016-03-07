(function() {
  'use strict';

  angular
    .module('Escalante')
    .run(run);
  
  run.$inject = ['$rootScope','$location','$http','AuthenticationService'];

  function run($rootScope, $location, $http,AuthenticationService) {
    $rootScope.$on('$locationChangeStart',locationChangeStart); 
    
    function locationChangeStart(event, next, current) {
      if (AuthenticationService.isLogged()) {
        $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa(AuthenticationService.getToken()+':');
      }
      $rootScope.isAuthenticated = AuthenticationService.isLogged();
      $rootScope.isAdmin = AuthenticationService.isAdmin();
      if ($location.path() !== '/login' && !AuthenticationService.isLogged()) {
        $location.path('/login');
      };
    }
  }

})();