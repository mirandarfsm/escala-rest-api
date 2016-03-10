( function(){

    angular
        .module('Escalante')
        .controller('CadastroUsuarioDetailController',CadastroUsuarioDetailController);

    CadastroUsuarioDetailController.$inject = ['usuarioGetOne','usuarioService','$location'];

    function CadastroUsuarioDetailController(usuarioGetOne,$location) {
        var vm = this;

        vm.usuario = usuarioGetOne;

        vm.salvar = salvar;

        function salvar() {
            vm.usuario.data_promocao = new Date(vm.data_promocao).getTime();
            vm.usuario.save().then(function(){
                $location.path('/cadastro-usuario');
            });
            //usuarioService.save(vm.usuario).success(function(){
            //});
        }
    }

})();
