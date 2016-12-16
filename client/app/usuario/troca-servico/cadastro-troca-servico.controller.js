(function(){
	'use strict';

  angular
    .module('Escalante')
    .controller('CadastroTrocaServicoController',CadastroTrocaServicoController);
  
  CadastroTrocaServicoController.$inject = ['trocaServicoGetList','trocaServicoPendenteGetList'];

  function CadastroTrocaServicoController(trocaServicoGetList,trocaServicoPendenteGetList){
    var vm = this;

    vm.tipos = ['Preta','Vermelha','Roxa'];
    vm.minhasTrocas = false;
    vm.trocaServicos = trocaServicoGetList;
	console.log(vm.trocaServicos[0])
    vm.trocaServicosPendentes = trocaServicoPendenteGetList;
    
   

    /*
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
    */
  }

  
})();