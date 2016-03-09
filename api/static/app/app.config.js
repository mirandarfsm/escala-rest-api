(function() {
  'use strict';

  angular
      .module("Escalante")
      .config(config);
  
  config.$inject = ['RestangularProvider'];
  
  function config(RestangularProvider) {
	  RestangularProvider.setBaseUrl('http://127.0.0.1:5000/api/v1.0/');
	  
	  RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
          var extractedData;
          if (operation === "getList") {
            extractedData = data.objects;
            extractedData.first = data.first;
            extractedData.last = data.last;
            extractedData.next = data.next;
            extractedData.page = data.page;
            extractedData.pages = data.pages;
            extractedData.per_page = data.per_page;
            extractedData.prev = data.prev;
            extractedData.total = data.total;   
          } else {
            extractedData = data.data;
          }
          return extractedData;
        });
  }
    
})();
