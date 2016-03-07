( function(){
    'use strict';

    angular 
        .module('Escalante')
        .controller('AuditoriaAfastamentoController',AuditoriaAfastamentoController);

    AuditoriaAfastamentoController.$inject = ['afastamentoGetList','afastamentoService'];
         
    function AuditoriaAfastamentoController(afastamentoGetList,afastamentoService){
        var vm = this;
        
        vm.afastamentos = afastamentoGetList.objects;

        vm.deletar = deletar;
        
        function deletar(index){
            var afastamento = self.afastamentos[index];
            afastamentoFactory.delete(afastamento.id).then(function(data){
                self.afastamentos.splice(index,1);
            });
        }

    }

})();