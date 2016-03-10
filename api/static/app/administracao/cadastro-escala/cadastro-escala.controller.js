( function(){
    'use strict';

    angular 
        .module('Escalante')
        .controller('CadastroEscalaController',CadastroEscalaController);

    CadastroEscalaController.$inject = ['escalaGetList'];
         
    function CadastroEscalaController(escalaGetList) {
        var vm = this;
        
        vm.escalas = escalaGetList.objects;
        
        vm.deletar = deletar;

        function deletar(index) {
            var escala = vm.escalas[index];
            escala.remove(escala.id).then(function () {
                vm.escalas.splice(index,1);
            });
        }   
    }

})();