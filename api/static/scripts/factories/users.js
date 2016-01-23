app.factory('userFactory', ['$http', function($http) {

    var urlBase = '/api/v1.0/usuarios/';
    var userFactory = {};

    userFactory.getUsers = function () {
        return $http.get(urlBase);
    };

    userFactory.getUser = function (id) {
        return $http.get(urlBase + id);
    };

    userFactory.insertUser = function (user) {
        return $http.post(urlBase, user);
    };

    userFactory.updateUser = function (user) {
        return $http.put(urlBase + user.id, user)
    };

    userFactory.deleteUser = function (id) {
        return $http.delete(urlBase + id);
    };
    
    userFactory.getServices = function (id) {
        return $http.get(urlBase + '/' + id + '/servico/');
    };
    /*userFactory.getOrders = function (id) {
        return $http.get(urlBase + '/' + id + '/orders');
    };
    */

    return userFactory;
}]);