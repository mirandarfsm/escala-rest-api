(function(){
  'use strict';

    angular
        .module('Escalante')
        .controller('CadastroTrocaServicoDetailController',CadastroTrocaServicoDetailController);
  
    CadastroTrocaServicoDetailController.$inject = [];

    function CadastroTrocaServicoDetailController($location,AuthenticationService,usuarioService){
        var vm = this;

        vm.trocaServico = {};

        vm.servicos = [];
        vm.salvar = salvar;
        
        function salvar() {
            vm.trocaServico.substituido = usuario;            
            autenticacaoService.all('troca/servico',vm.trocaServico).success(function() {
                $location.path('/cadastro-troca-servico');
            });
        }
    }

  
});