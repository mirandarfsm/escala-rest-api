var app = angular.module("Escalante",['ngRoute','ui.bootstrap','ngSanitize','ui.select']);

app.config(function($routeProvider) {
  
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
  })
  
  // cadastro de usuario
  .when('/cadastro-usuario', {
    templateUrl: 'pages/cadastro-usuario-list.html',
    controller: 'CadastroUsuarioCtrl',
    controllerAs: 'cadastroUsuarioCtrl'
  })
  .when('/cadastro-usuario/new', {
    templateUrl: 'pages/cadastro-usuario-form.html',
    controller: 'CadastroUsuarioNewCtrl',
    controllerAs: 'cadastroUsuarioCtrl'
  })
  .when('/cadastro-usuario/:id', {
    templateUrl: 'pages/cadastro-usuario-form.html',
    controller: 'CadastroUsuarioDetailCtrl',
    controllerAs: 'cadastroUsuarioCtrl'
  })

  // cadastro de escala
  .when('/cadastro-escala', {
    templateUrl: 'pages/cadastro-escala-list.html',
    controller: 'CadastroEscalaCtrl',
    controllerAs: 'cadastroEscalaCtrl'
  })
  .when('/cadastro-escala/new', {
    templateUrl: 'pages/cadastro-escala-form.html',
    controller: 'CadastroEscalaNewCtrl',
    controllerAs: 'cadastroEscalaCtrl'
  })
  .when('/cadastro-escala/:id', {
    templateUrl: 'pages/cadastro-escala-form.html',
    controller: 'CadastroEscalaDetailCtrl',
    controllerAs: 'cadastroEscalaCtrl'
  })
  
  // cadastro de servico
  .when('/cadastro-servico', {
    templateUrl: 'pages/cadastro-servico-form.html',
    controller: 'CadastroServicoCtrl',
    controllerAs: 'cadastroServicoCtrl'
  })
  .when('/cadastro-servico/new', {
    templateUrl: 'pages/cadastro-servico-form.html',
    controller: 'CadastroServicoNewCtrl',
    controllerAs: 'cadastroServicoCtrl'
  })
  .when('/cadastro-servico/:id', {
    templateUrl: 'pages/cadastro-servico-form.html',
    controller: 'CadastroServicoDetailCtrl',
    controllerAs: 'cadastroServicoCtrl'
  })
  
  // cadastro de afastamento
  .when('/cadastro-afastamento', {
    templateUrl: 'pages/cadastro-afastamento-list.html',
    controller: 'CadastroAfastamentoCtrl',
    controllerAs: 'cadastroAfastamentoCtrl'
  })
  .when('/cadastro-afastamento/new', {
    templateUrl: 'pages/cadastro-afastamento-form.html',
    controller: 'CadastroAfastamentoNewCtrl',
    controllerAs: 'cadastroAfastamentoCtrl'
  })
  .when('/cadastro-afastamento/:id', {
    templateUrl: 'pages/cadastro-afastamento-form.html',
    controller: 'CadastroAfastamentoDetailCtrl',
    controllerAs: 'cadastroAfastamentoCtrl'
  })

  // cadastro de troca de servico
  .when('/cadastro-troca-servico', {
    templateUrl: 'pages/cadastro-troca-servico-list.html',
    controller: 'CadastroTrocaServicoCtrl',
    controllerAs: 'cadastroTrocaServicoCtrl'
  })
  .when('/cadastro-troca-servico/new', {
    templateUrl: 'pages/cadastro-troca-servico-form.html',
    controller: 'CadastroTrocaServicoNewCtrl',
    controllerAs: 'cadastroTrocaServicoCtrl'
  })

  // Gerencia de Afastamento
  .when('/gerencia-afastamento', {
    templateUrl: 'pages/gerencia-afastamento-list.html',
    controller: 'GerenciaAfastamentoCtrl',
    controllerAs: 'gerenciaAfastamentoCtrl'
  })
  .when('/gerencia-afastamento/:id', {
    templateUrl: 'pages/gerencia-afastamento-form.html',
    controller: 'GerenciaAfastamentoDetailCtrl',
    controllerAs: 'gerenciaAfastamentoCtrl'
  })

 .when('/perfil-usuario', {
    templateUrl: 'pages/perfil-usuario-form.html',
    controller: 'PerfilUsuarioCtrl',
    controllerAs: 'perfilUsuarioCtrl'
  })

  .when('/servicos', {
    templateUrl: 'pages/servico-lista.html',
    controller: 'ServicosCrtl',
    controllerAs: 'servicosCtrl'
  })
  .otherwise({ redirectTo: '/' });
});

app.run(function ($rootScope, $location, $http,AuthenticationService) {
  $rootScope.$on('$locationChangeStart', function (event, next, current) {
    if (AuthenticationService.isLogged()) {
      $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa(AuthenticationService.getToken()+':');
    }
    $rootScope.isAuthenticated = AuthenticationService.isLogged();
    $rootScope.isAdmin = AuthenticationService.isAdmin();
    if ($location.path() !== '/login' && !AuthenticationService.isLogged()) {
      $location.path('/login');
    };
  });
});