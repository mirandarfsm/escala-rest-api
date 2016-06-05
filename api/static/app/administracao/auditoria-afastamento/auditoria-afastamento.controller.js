( function(){
    'use strict';

    angular 
        .module('Escalante')
        .controller('AuditoriaAfastamentoController',AuditoriaAfastamentoController);

    AuditoriaAfastamentoController.$inject = ['afastamentoGetList'];
         
    function AuditoriaAfastamentoController(afastamentoGetList){
        var vm = this;
        
        vm.afastamentos = afastamentoGetList;
        vm.deletar = deletar;
        
        function deletar(index){
            var afastamento = vm.afastamentos[index];
            afastamento.remove().then(function(data){
                vm.afastamentos.splice(index,1);
            });
        }

    }

})();