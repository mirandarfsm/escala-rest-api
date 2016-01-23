var app = angular.module("Escalante",['ngRoute','ui.bootstrap','ngSanitize','ui.select']);

app.config(function($routeProvider) {
  
  $routeProvider
  .when("/", {
    templateUrl: 'pages/teste.html',
    controller: 'TesteCtrl',
    controllerAs: 'ctrl'
  })
  .when('/login',{
    templateUrl: 'pages/login.html',
    controller: 'LoginCtrl',
    controllerAs: 'loginCtrl',
    allowAnonymous: true
  })
  .when('/cadastro-usuario', {
    templateUrl: 'pages/cadastro-usuario.html',
    controller: 'CadastroUsuarioCtrl',
    controllerAs: 'cadastroUsuarioCtrl'
  })
  .when('/cadastro-escala', {
    templateUrl: 'pages/cadastro-escala.html',
    controller: 'CadastroEscalaCtrl',
    controllerAs: 'cadastroEscalaCtrl'
  })
  .when('/cadastro-servico', {
    templateUrl: 'pages/cadastro-servico.html',
    controller: 'CadastroServicoCtrl',
    controllerAs: 'cadastroServicoCtrl'
  })
  .when('/cadastro-afastamento', {
    templateUrl: 'pages/cadastro-afastamento.html',
    controller: 'CadastroAfastamentoCtrl',
    controllerAs: 'cadastroAfastamentoCtrl'
  })
  .when('/associacao-escala', {
    templateUrl: 'pages/associacao-escala.html',
    controller: 'AssociacaoEscalaCtrl',
    controllerAs: 'associacaoEscalaCtrl'
  })
  .otherwise({ redirectTo: '/' });
});

app.run(function ($rootScope, $location, $http,AuthenticationService) {

  if (AuthenticationService.isLogged()) {
    $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa(AuthenticationService.getToken+':');
  }

  $rootScope.$on('$locationChangeStart', function (event, next, current) {
     $rootScope.isAuthenticated = AuthenticationService.isLogged();
    if ($location.path() !== '/login' && !AuthenticationService.isLogged()) {
      $location.path('/login');
    };
  });
});