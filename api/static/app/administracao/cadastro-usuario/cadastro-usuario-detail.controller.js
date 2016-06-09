(function() {
    'use strict';
    
    angular
        .module('Escalante')
        .controller('CadastroUsuarioDetailController',CadastroUsuarioDetailController);

    CadastroUsuarioDetailController.$inject = ['usuarioGetOne','$location'];

    function CadastroUsuarioDetailController(usuarioGetOne,$location) {
        var vm = this;
        
        vm.usuario = usuarioGetOne;
        vm.usuario.data_promocao = vm.usuario.data_promocao !== undefined ? new Date(vm.usuario.data_promocao):undefined;
        vm.popup = false;
        vm.perfis = [
                     { nome:'Administrador', valor:0},
                     { nome:'Escalante', valor:1},
                    ];
        
        vm.open = open;
        vm.salvar = salvar;

        function open(){
             vm.popup = true;
        }

        function salvar() {
        	if(!vm.usuario.id) vm.usuario.password = vm.usuario.username; 
            vm.usuario.save().then(function(){
                $location.path('/cadastro-usuario');
            });
        }
    }

})();
