(function() {
  'use strict';

  angular
      .module("Escalante")
      .config(config);

  config.$inject = ['$routeProvider'];

  function config($routeProvider) {
    Restangular.setBaseUrl('http://127.0.0.1:5000/api/v1.0/');
    
    $routeProvider
    .when("/", {
      templateUrl: 'pages/teste.html',
      controller: 'TesteCtrl',
      controllerAs: 'ctrl'
    })
    // login
    .when('/login',{
      templateUrl: 'pages/login.html',
      controller: 'LoginCtrl',
      controllerAs: 'loginCtrl',
      allowAnonymous: true
    });
})();
