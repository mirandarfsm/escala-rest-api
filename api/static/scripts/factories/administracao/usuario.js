app.factory('administracaoUsuarioFactory', ['$http', function($http) {

    var urlBase = '/api/v1.0/administracao/usuarios/';
    var service = {};

    service.getAll = function () {
        return $http.get(urlBase);
    };

    service.get = function (id) {
        return $http.get(urlBase + id);
    };

    service.insert = function (user) {
        return $http.post(urlBase, user);
    };

    service.update = function (user) {
        return $http.put(urlBase + user.id, user)
    };

    service.delete = function (id) {
        return $http.delete(urlBase + id);
    };
    
    service.getServicos = function (id) {
        return $http.get(urlBase  + id + '/servico/');
    };

    service.getAfastamentos = function (id) {
        return $http.get(urlBase + id + '/afastamento/');
    };
    /*userFactory.getOrders = function (id) {
        return $http.get(urlBase + '/' + id + '/orders');
    };
    */

    return service;
}]);