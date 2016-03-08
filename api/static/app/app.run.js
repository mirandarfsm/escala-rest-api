(function() {
  'use strict';

  angular
    .module('Escalante')
    .run(run);
  
  run.$inject = ['$rootScope','$location','$http','autenticacaoService'];

  function run($rootScope, $location, $http,autenticacaoService) {
    $rootScope.$on('$locationChangeStart',locationChangeStart); 
    
    function locationChangeStart(event, next, current) {
      if (autenticacaoService.isLogged()) {
        $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa(autenticacaoService.getToken()+':');
      }
      $rootScope.isAuthenticated = autenticacaoService.isLogged();
      $rootScope.isAdmin = autenticacaoService.isAdmin();
      if ($location.path() !== '/login' && !autenticacaoService.isLogged()) {
        $location.path('/login');
      };
    }
  }

})();