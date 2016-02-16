app.factory('usuarioFactory', ['$http', function($http) {

    var urlBase = '/api/v1.0/usuario';
    var service = {};

    service.get = function () {
        return $http.get(urlBase+"/");
    };

    service.update = function () {
        return $http.put(urlBase+"/")
    };

    service.getServicos = function () {
        return $http.get(urlBase  + '/servicos/');
    };

    service.getServicosDetail = function (id) {
        return $http.get(urlBase  + '/servicos/' + id);
    };

    service.getAfastamentos = function (id) {
        return $http.get(urlBase + '/afastamentos/');
    };

    service.getAfastamentosDetail = function (id) {
        return $http.get(urlBase + '/afastamentos/' + id);
    };

    service.getEscalas = function () {
        return $http.get(urlBase + '/escalas/');
    };

    service.getEscalasDetail = function (id) {
        return $http.get(urlBase + '/escalas/' + id);
    };

    service.insertAfastamento = function(afastamento){
        return $http.post(urlBase + '/afastamentos/', afastamento);
    };

    service.updateAfastamento = function(afastamento){
        return $http.put(urlBase + '/afastamentos/' + afastamento.id, afastamento);
    };

    service.insertTrocaServico = function(trocaServico){
        return $http.post(urlBase + '/servico/troca/',trocaServico);
    };

    service.updateTrocaServico = function(trocaServico){
        return $http.put(urlBase + '/servico/troca/' + trocaServico.id,trocaServico);
    };

    service.deleteAfastamento = function(id){
        return $http.delete(urlBase + '/afastamentos/' + id);
    };

    service.deleteTrocaServico = function(id){
        return $http.delete(urlBase + '/servico/troca/' + id);
    };

    return service;
}]);