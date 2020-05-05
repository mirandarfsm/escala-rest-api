(function() {
    'use strict';

    angular
        .module('Escalante')
        .controller('CadastroServicoDetailController', CadastroServicoDetailController);

    CadastroServicoDetailController.$inject = ['servicoGetOne', 'escalaGetList', 'escalaService', '$location'];

    function CadastroServicoDetailController(servicoGetOne, escalaGetList, escalaService, $location) {
        var vm = this;

        vm.servico = servicoGetOne;
        vm.escalas = escalaGetList;
        vm.popupDataServico = false;
        vm.tiposServico = [
            { id: 0, nome: 'Preta' },
            { id: 1, nome: 'Vermelha' },
            { id: 2, nome: 'Roxa' }
        ];

        vm.openDataServico = openDataServico;
        vm.onEscalaChange = onEscalaChange;
        vm.salvar = salvar;

        function openDataServico() {
            vm.popupDataServico = true;
        }

        function onEscalaChange(escala, model) {
            escalaService.one(escala.id)
                .getList('usuario-escala')
                .then(function(data) {
                    vm.listUsuarioEscala = data;
                });
        }

        function salvar() {
            vm.servico.tipo = vm.servico.tipo.id
            vm.servico.data = new Date(vm.servico.data);
            vm.servico.save().then(function() {
                $location.path('/gerencia-servico');
            });
        }

    }

})();