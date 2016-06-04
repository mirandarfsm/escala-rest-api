(function(){
	'use strict';

  angular
    .module('Escalante')
    .controller('CadastroTrocaServicoController',CadastroTrocaServicoController);
  
  CadastroTrocaServicoController.$inject = [];

  function CadastroTrocaServicoController(AuthenticationService,usuarioService){
    var vm = this;

    vm.tipos = ['Preta','Vermelha','Roxa'];
    vm.minhasTrocas = false;
    vm.trocaServicos = [];
    vm.trocaServicosPendentes = [];
    
    vm.aceitar = aceitar;
    vm.deletar = deletar;

    function aceitar(index) {
        var trocaServico = vm.trocaServicosPendentes[index]
        usuarioService.acceptTrocaServico(trocaServico.id).success(function () {
            vm.trocaServicosPendentes.splice(index,1);
        });
    }

    function deletar(index) {
        var trocaServico = vm.trocaServicos[index]
        usuarioService.deleteTrocaServico(trocaServico.id).success(function () {
            vm.trocaServicos.splice(index,1);
        });
    }
  }

  
})();