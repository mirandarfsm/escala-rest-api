(function(){
	'use strict';

	angular
		.module('Escalante')
		.controller('CalendarioServicoController',CalendarioServicoController)
	
	CalendarioServicoController.$inject = ['servicoGetList','afastamentoGetList'];
	
	function CalendarioServicoController(servicoGetList,afastamentoGetList){
		var vm = this;

		var servicos = servicoGetList;
		var afastamentos = afastamentoGetList;
		
		vm.eventSources = [servicoEvents(servicos),afastamentoEvents(afastamentos)];
		vm.uiConfig = {
			calendar:{
				height: 450,
				editable: false
			},
		};
		
		function servicoEvents(servicos) {
			var events = [];
			var tipoServico = ['black','red','purple'];
			servicos.forEach(function(servico){
				var escala = servico.usuario_escala.escala;
				var usuario = servico.usuario_escala.usuario;
				events.push({
					id: servico.id,
					title: usuario.nome_guerra + " " + usuario.posto + " " + usuario.especialidade + " - " + escala.nome,
					start: servico.data, 
					allDay: true,
					color: tipoServico[servico.tipo]
				})
			});
			return events;
		};
		
		function afastamentoEvents(afastamentos) {
	        var events = [];
	        afastamentos.forEach(function(afastamento){
	          events.push({
	        	id: afastamento.id,
	            title: afastamento.usuario.nome_guerra+': '+afastamento.motivo,
	            start: afastamento.data_inicio,
	            end: afastamento.data_fim,
	            allDay: true,
	            color: afastamento.ativo ? 'blue' : 'gray'
	            });
	        });
	        return events;
	      };
	}
	
})();