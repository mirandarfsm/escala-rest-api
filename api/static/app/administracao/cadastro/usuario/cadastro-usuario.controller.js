( function(){

    angular
        .module('Escalante')
        .controller('CadastroUsuarioController',CadastroUsuarioController);

    CadastroUsuarioController.$inject = ['usuarioGetList','usuarioService'];

    function CadastroUsuarioController(usuarioGetList,usuarioService) {
        var vm = this;
        
        vm.usuarios = usuarioGetList.objects;
    
        vm.deletar = deletar;

        function deletar(index) {
            var usuario = self.usuarios[index]
            userFactory.delete(usuario.id).success(function () {
                self.usuarios.splice(index,1);
            });
        }
    }

})();
