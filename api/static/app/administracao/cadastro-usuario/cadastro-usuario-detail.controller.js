( function(){

    angular
        .module('Escalante')
        .controller('CadastroUsuarioDetailController',CadastroUsuarioDetailController);

    CadastroUsuarioDetailController.$inject = ['usuarioGetOne','$location'];

    function CadastroUsuarioDetailController(usuarioGetOne,$location) {
        var vm = this;

        vm.usuario = usuarioGetOne;
        vm.popup = false;

        vm.open = open;
        vm.salvar = salvar;
   
        function open(){
             vm.popup = true;
        }

        function salvar() {
            vm.usuario.save().then(function(){
                $location.path('/cadastro-usuario');
            });
        }
    }

})();
