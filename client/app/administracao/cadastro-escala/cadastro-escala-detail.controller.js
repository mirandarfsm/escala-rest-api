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
        vm.escala.usuarios = vm.escala.id ? vm.escala.getList('usuario').$object : undefined;
        vm.escala.vermelhas = vm.escala.datas_especiais ? getDatas(vm.escala.datas_especiais,1) : [];
        vm.escala.roxas = vm.escala.datas_especiais ? getDatas(vm.escala.datas_especiais,2) : [];
        vm.popupVermelha = false;
        vm.popupRoxa = false;
        
        vm.dataRoxa = undefined;
        vm.dataVermelha = undefined;
        
        vm.novaDataVermelha = novaDataVermelha;
        vm.adicionarDataVermelha = adicionarDataVermelha;
        vm.novaDataRoxa = novaDataRoxa;
        vm.adicionarDataRoxa = adicionarDataRoxa;

        vm.openVermelha = openVermelha;
        vm.openRoxa = openRoxa;
        
        vm.salvar = salvar;
        
        function openVermelha(){
            vm.popupVermelha = true;
        }
        
        function openRoxa(){
            vm.popupRoxa = true;
        }

        function novaDataVermelha(){
        	vm.dataVermelha = new Date();
        }
        
        function adicionarDataVermelha(){
        	var object = {};
        	object.data = vm.dataVermelha;
        	object.tipo = 1;
            vm.escala.vermelhas.push(object);
            vm.dataVermelha = undefined;
        }
        
        function novaDataRoxa(){
        	vm.dataRoxa = new Date();
        }
        
        function adicionarDataRoxa(){
        	var object = {};
        	object.data = vm.dataRoxa;
        	object.tipo = 2;
            vm.escala.roxas.push(object);
            vm.dataRoxa = undefined;
        }
        
        function salvar() {
        	vm.escala.datas_especiais = vm.escala.roxas.concat(vm.escala.vermelhas);
        	console.log(vm.escala.datas_especiais);
            vm.escala.save().then(function(){
                $location.path('/cadastro-escala');
            });
        }
        
        function getDatas(datas,tipo){
        	var list_date = [];
        	datas.forEach(function(data){
        		if (data.tipo === tipo){
        			data.data = new Date(data.data); 
        			list_date.push(data);
        		}
        	});
        	return list_date;
        }
    }
    

})();