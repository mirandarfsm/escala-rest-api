(function(){
	'use strict';

    angular
        .module('Escalante')
        .controller('CadastroTrocaServicoDetailController',CadastroTrocaServicoDetailController);
  
    CadastroTrocaServicoDetailController.$inject = ['trocaServicoGetOne','servicoGetList','$location'];

    function CadastroTrocaServicoDetailController(trocaServicoGetOne,servicoGetList,$location){
        var vm = this;

        vm.trocaServico = trocaServicoGetOne;
        vm.servicos = servicoGetList;
        
        vm.salvar = salvar;
        
        function salvar() {
            vm.trocaServico.save().then(function() {
                $location.path('/cadastro-troca-servico');
            });
        }
    }

  
})();