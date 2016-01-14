var app = angular.module("Escalante",['ngRoute','ui.bootstrap']);

app.config(function($routeProvider) {
  
  $routeProvider
  .when("/", {
    templateUrl: 'pages/teste.html'
    //controller: 'TesteCtrl',
    //controllerAs: 'teste'
  })
  .when('/login',{
    templateUrl: 'pages/login.html',
    controller: 'LoginCtrl',
    controllerAs: 'loginCtrl'
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
  .when('/associacao-escala', {
    templateUrl: 'pages/associacao-escala.html',
    controller: 'AssociacaoEscalaCtrl',
    controllerAs: 'associacaoEscalaCtrl'
  })
  .otherwise('/');
});