(function() {
    'use strict';

    angular
        .module("Escalante")
        .config(config);

    config.$inject = ['RestangularProvider', '$httpProvider'];

    function config(RestangularProvider, $httpProvider) {
        RestangularProvider.setBaseUrl('/api/v1.0/');
        RestangularProvider.setRequestSuffix('/');

        RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
            var extractedData;
            if (operation === "getList") {
                extractedData = data.objects;
                extractedData.meta = data.meta;
            } else {
                extractedData = data;
            }
            return extractedData;
        });

        $httpProvider.interceptors.push('httpErrorInterceptor');
    }

})();