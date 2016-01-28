app.factory('escalaFactory', ['$http', function($http) {

    var urlBase = '/api/v1.0/escalas/';
    var escalaFactory = {};

    escalaFactory.getEscalas = function () {
        return $http.get(urlBase);
    };

    escalaFactory.getEscala = function (id) {
        return $http.get(urlBase + id);
    };

    escalaFactory.insertEscala = function (obj) {
        return $http.post(urlBase, obj);
    };

    escalaFactory.updateEscala = function (obj) {
        return $http.put(urlBase + obj.id, obj)
    };

    escalaFactory.deleteEscala = function (id) {
        return $http.delete(urlBase + id);
    };
    
    escalaFactory.getUsuarios = function (id) {
        return $http.get(urlBase + id + '/usuario/');
    };
    
    escalaFactory.generateServices = function(id){
        return $http.get(urlBase + id + '/generate/');
    };

    return escalaFactory;
}]);