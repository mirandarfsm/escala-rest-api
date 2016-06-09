(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('GerenciaServicoController',GerenciaServicoController);
	
	GerenciaServicoController.$inject = ['escalaGetList','escalaService','$location'];
	
	function GerenciaServicoController(escalaGetList){
		var vm = this;
		
		vm.escalas = escalaGetList;
		vm.tipos = ['Preto','Vermelho','Roxo'];
		var tipoServico = ['black','red','purple'];

		vm.uiConfig = {
			calendar:{
				height: 450,
				editable: true
			}
		};
		
		vm.getServicos = getServicos;

		function getServicos(){
			vm.escala.getList('servico').then(function(data){				
				vm.servicos = data;
				vm.eventSources = [servicoEvents(vm.servicos),vm.events];
			});
			//vm.servicos = vm.escala.getList('servico');
		}
  
		function servicoEvents(servicoList) {
			var events = [];
			servicoList.forEach(function(servico){
				var usuario = servico.usuario_escala.usuario;
				events.push({
					title: usuario.nome_guerra + " " + usuario.posto + " " + usuario.especialidade,
					start: servico.data, 
					allDay: true,
					color: tipoServico[servico.tipo]
				})
			});
			return events;
		};

	}
	
})();