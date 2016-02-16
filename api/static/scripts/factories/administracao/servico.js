app.factory('servicoFactory', ['$http', function($http) {

    var urlBase = '/api/v1.0/administracao/servicos/';
    var service = {};

    service.getAll = function () {
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

    service.deleteAll = function () {
        return $http.delete(urlBase);
    };
    
    service.delete = function (id) {
        return $http.delete(urlBase + id);
    };
    
    service.getUsuarios = function (id) {
        return $http.get(urlBase + id + '/usuario');
    };



    return service;
}]);