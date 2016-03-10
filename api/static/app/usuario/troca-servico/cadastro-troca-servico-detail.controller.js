(function(){
  'use strict';

    angular
        .module('Escalante')
        .controller('CadastroTrocaServicoDetailController',CadastroTrocaServicoDetailController);
  
    CadastroTrocaServicoDetailController.$inject = [];

    function CadastroTrocaServicoDetailController(trocaServicoGetOne,$location,AuthenticationService){
        var vm = this;

        vm.trocaServico = trocaServicoGetOne;
        vm.servicos = [];
        
        vm.salvar = salvar;
        
        function salvar() {
            vm.trocaServico.substituido = usuario;            
            vm.trocaServico.save().then(function() {
                $location.path('/cadastro-troca-servico');
            });
        }
    }

  
});