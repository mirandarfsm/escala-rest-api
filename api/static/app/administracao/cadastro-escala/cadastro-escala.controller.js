( function(){
    'use strict';

    angular 
        .module('Escalante')
        .controller('CadastroEscalaController',CadastroEscalaController);

    CadastroEscalaController.$inject = ['escalaGetList','escalaService'];
         
    function CadastroEscalaController(escalaGetList,escalaService) {
        var vm = this;
        
        vm.deletar = deletar;
        vm.escalas = escalaGetList.objects;

        function deletar(index) {
            var escala = self.escalas[index]
            escalaService.delete(escala.id).success(function () {
                self.escalas.splice(index,1);
            });
        }   
    }

})();