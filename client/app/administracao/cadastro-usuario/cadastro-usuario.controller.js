( function(){

    angular
        .module('Escalante')
        .controller('CadastroUsuarioController',CadastroUsuarioController);

    CadastroUsuarioController.$inject = ['usuarioGetList'];

    function CadastroUsuarioController(usuarioGetList) {
        var vm = this;
        
        vm.usuarios = usuarioGetList;
        
        vm.deletar = deletar;

        function deletar(index) {
            var usuario = vm.usuarios[index];
            usuario.remove().then(function () {
                vm.usuarios[index].ativo = !vm.usuarios[index].ativo;
            });
        }
    }

})();
