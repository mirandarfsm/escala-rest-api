( function(){

    angular
        .module('Escalante')
        .controller('CadastroUsuarioDetailController',CadastroUsuarioDetailController);

    CadastroUsuarioDetailController.$inject = ['usuarioGetOne','usuarioService','$location'];

    function CadastroUsuarioDetailController(usuarioGetOne,usuarioService,$location) {
        var vm = this;

        vm.usuario = usuarioGetOne;

        vm.salvar = salvar;

        function salvar() {
            self.usuario.data_promocao = new Date(vm.data_promocao).getTime();
            usuarioService.put(vm.usuario).success(function(){
                $location.path('/cadastro-usuario');
            });
        }
    }

})();
