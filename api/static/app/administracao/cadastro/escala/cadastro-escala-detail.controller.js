(function() {
    'use strict';

    angular
        .module('Escalante')
        .controller('CadastroEscalaDetailController',CadastroEscalaDetailController); 

    CadastroEscalaDetailController.$inject = ['escalaGetOne','$location','escalaService','usuarioGetList'];

    function CadastroEscalaDetailController(escalaGetOne,$location,escalaService,usuarioGetList) {
        var vm = this
        
        vm.usuarios = usuarioGetList.objects;
        vm.escala = escalaGetOne.escala;
        
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
            //self.usuario.data_promocao = new Date(self.data_promocao).getTime();
            escalaService.put(vm.escala).success(function(){
                $location.path('/cadastro-escala');
            });
        }
    }

})();