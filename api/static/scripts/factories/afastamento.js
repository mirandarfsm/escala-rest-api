app.factory('afastamentoFactory', ['$http', function($http) {

    var urlBase = '/api/v1.0/afastamentos/';
    var service = {};

    service.get = function () {
        return $http.get(urlBase);
    };

    service.get = function (id) {
        return $http.get(urlBase + id);
    };

    service.insert = function (obj) {
        return $http.post(urlBase, obj);
    };

    service.update = function (obj) {
        return $http.put(urlBase + obj.id, obj)
    };

    service.delete = function (id) {
        return $http.delete(urlBase + id);
    };
    
    service.getUsuarios = function (id) {
        return $http.get(urlBase + id + '/usuario');
    };

    /*userFactory.getOrders = function (id) {
        return $http.get(urlBase + '/' + id + '/orders');
    };
    */

    return service;
}]);