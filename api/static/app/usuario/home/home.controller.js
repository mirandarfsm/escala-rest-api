(function() {
  'use strict';

  angular
      .module("Escalante")
      .controller('HomeController',HomeController);
  
  HomeController.$inject = ['$rootScope','servicoGetList','afastamentoGetList'];
  
  function HomeController($rootScope,servicoGetList,afastamentoGetList) {
	  var vm = this;
      var servicoList = servicoGetList;
      var tipoServico = ['black','red','purple'];
      var afastamentoList = afastamentoGetList;
      
	  vm.eventSources = [servicoEvents(servicoList),afastamentoEvents(afastamentoList)];
      vm.menorServico = getMenorData(servicoList);
      vm.uiConfig = {
        calendar:{
          height: 450,
          editable: false
        }
      };
      
      function servicoEvents(servicoList) {
        var events = [];
        servicoList.forEach(function(servico){
          events.push({
            title: servico.usuario_escala.escala.nome,
            start: servico.data,
            allDay: true,
            color: tipoServico[servico.tipo]})
        });
        return events;
      };
      
      function afastamentoEvents(afastamentos) {
        var events = [];
        afastamentos.forEach(function(afastamento){
          events.push({
            title: afastamento.motivo,
            start: afastamento.data_inicio,
            end: afastamento.data_fim,
            allDay: true,
            color: afastamento.ativo ? 'blue' : 'gray'
            });
        });
        return events;
      };
      
      function getMenorData(servicos) {
        var menor;
        servicos.forEach(function(servico){
          if (menor === undefined) {
            menor = servico;
          }else if (menor.data > servico.data) {
            menor = servico;
          }
        });
        return menor;
      }
      
  }
    
})();