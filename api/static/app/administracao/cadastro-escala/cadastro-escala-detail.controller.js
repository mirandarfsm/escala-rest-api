(function() {
    'use strict';

    angular
        .module('Escalante')
        .controller('CadastroEscalaDetailController',CadastroEscalaDetailController); 

    CadastroEscalaDetailController.$inject = ['escalaGetOne','$location','usuarioGetList'];

    function CadastroEscalaDetailController(escalaGetOne,$location,usuarioGetList) {
        var vm = this;

        vm.usuarios = usuarioGetList;
        vm.escala = escalaGetOne;
        
        vm.adicionarFeriado = adicionarFeriado;
        vm.adicionarRoxa = adicionarRoxa;
        vm.removerFeriado = removerFeriado;
        vm.removerRoxa = removerRoxa;
        vm.salvar = salvar;
        
        function adicionarFeriado(){
            if (!vm.escala.feriados){
                vm.escala.feriados = [];
            }
            vm.escala.feriados.push(new Date);
        }

        function adicionarRoxa(){
            if (!vm.escala.roxas){
                vm.escala.roxas = [];
            }
            vm.escala.roxas.push(new Date);
        }

        function removerFeriado(index){
            vm.escala.feriados.splice(index,1);
        }

        function removerRoxa(index){
            vm.escala.roxas.splice(index,1);
        }
        
        function salvar() {
            vm.escala.save().then(function(){
                $location.path('/cadastro-escala');
            });
        }
    }

})();