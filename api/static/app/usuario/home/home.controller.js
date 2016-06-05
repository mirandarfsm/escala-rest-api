(function() {
  'use strict';

  angular
      .module("Escalante")
      .controller('HomeController',HomeController);
  
  HomeController.$inject = ['$rootScope','servicoGetList','afastamentoGetList'];
  
  function HomeController($rootScope,servicoGetList,afastamentoGetList) {
	  var vm = this;
      var servicolist = servicoGetList;
      
      var servicos = {
        events: [{title: 'Brejauveira',start: new Date(),allDay: true,color: 'red'}]
      }
      var afastamentos = [];
	  vm.eventSources = [servicos];
      
      vm.uiConfig = {
        calendar:{
          height: 450,
          width: 450,
          editable: false
        }
      };
  }
    
})();