( function(){
    'use strict';

    angular 
        .module('Escalante')
        .controller('CadastroEscalaController',CadastroEscalaController);

    CadastroEscalaController.$inject = ['escalaGetList'];
         
    function CadastroEscalaController(escalaGetList) {
        var vm = this;
        
        vm.escalas = escalaGetList;
        
        vm.deletar = deletar;

        function deletar(index) {
            var escala = vm.escalas[index];
            escala.remove(escala.id).then(function () {
                vm.escalas[index].ativo = !vm.escalas[index].ativo;
            });
        }   
    }

})();