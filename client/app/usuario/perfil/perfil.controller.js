(function() {
    'use strict';

    angular
        .module('Escalante')
        .controller('PerfilUsuarioController', PerfilUsuarioController)
        .controller('TrocaSenhaModalController', TrocaSenhaModalController);

    PerfilUsuarioController.$inject = ['$uibModal', 'passwordChangeOne'];
    TrocaSenhaModalController.$inject = ['$uibModalInstance', 'passwordChangeOne'];

    function PerfilUsuarioController($uibModal, passwordChangeOne) {
        var vm = this;
        vm.show = show;

        function show() {
            $uibModal.open({
                templateUrl: 'troca-senha-modal.html',
                controller: 'TrocaSenhaModalController',
                controllerAs: 'vm',
                resolve: {
                    passwordChangeOne: passwordChangeOne.clone()
                }
            });
        }
    }

    function TrocaSenhaModalController($uibModalInstance, passwordChangeOne) {
        var vm = this;

        vm.password = passwordChangeOne;

        vm.salvar = salvar;
        vm.cancel = cancel;

        function salvar() {
            vm.password.put().then(function() {
                $uibModalInstance.dismiss('cancel');
            });
        }

        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }
    }

})();