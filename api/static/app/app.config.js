(function() {
  'use strict';

  angular
      .module("Escalante")
      .config(config);
  
  config.$inject = ['Restangular'];
  
  function config(Restangular) {
	  Restangular.setBaseUrl('http://127.0.0.1:5000/api/v1.0/');
  }
    
})();
