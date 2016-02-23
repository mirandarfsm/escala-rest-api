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

    service.getTrocaServico = function () {
        return $http.get(urlBase + '/troca/servico/');
    };

    service.getTrocaServicoPendentes = function (id) {
        return $http.get(urlBase + '/troca/servico/pendentes/');
    };

    service.getTrocaServicoDetail = function (id) {
        return $http.get(urlBase + '/troca/servico/' + id);
    };


    service.insertAfastamento = function(afastamento){
        return $http.post(urlBase + '/afastamentos/', afastamento);
    };

    service.updateAfastamento = function(afastamento){
        return $http.put(urlBase + '/afastamentos/' + afastamento.id, afastamento);
    };

    service.insertTrocaServico = function(trocaServico){
        return $http.post(urlBase + '/troca/servico/',trocaServico);
    };

    service.updateTrocaServico = function(trocaServico){
        return $http.put(urlBase + '/troca/servico/' + trocaServico.id,trocaServico);
    };

    service.acceptTrocaServico = function(id){
        return $http.put(urlBase + '/troca/servico/' + id + '/aceitar/');
    };

    service.deleteAfastamento = function(id){
        return $http.delete(urlBase + '/afastamentos/' + id);
    };

    service.deleteTrocaServico = function(id){
        return $http.delete(urlBase + '/troca/servico/' + id);
    };

    return service;
}]);