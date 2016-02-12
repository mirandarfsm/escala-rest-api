app.factory('escalaFactory', ['$http', function($http) {

    var urlBase = '/api/v1.0/escalas/';
    var escalaFactory = {};

    escalaFactory.getAll = function () {
        return $http.get(urlBase);
    };

    escalaFactory.get = function (id) {
        return $http.get(urlBase + id);
    };

    escalaFactory.insert = function (obj) {
        return $http.post(urlBase, obj);
    };

    escalaFactory.update = function (obj) {
        return $http.put(urlBase + obj.id, obj)
    };

    escalaFactory.delete = function (id) {
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