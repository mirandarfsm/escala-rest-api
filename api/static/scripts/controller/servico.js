app.controller("CadastroServicoCtrl", function(escalaFactory){
    var self = this;
    getEscala();
    function getEscala(){
        escalaFactory.getEscalas()
           .success(function (data, status, headers, config) {
               self.escalas = data.escalas;
           })
           .error(function (error) {
               self.alert = {'msg':'Unable to load escalas: ' + error.message, 'type': 'danger'};
           });
    };
});

app.controller("TrocaServicoCtrl",function(userFactory){
    var self = this;
    self.tipos = ['Preta','Vermelha','Roxa'];
    
    function getServico(){
        userFactory.getServices(AuthenticationService.getUsuario().id)
           .success(function (data, status, headers, config) {
               self.escalas = data.servicos;
           })
           .error(function (error) {
               self.alert = {'msg':'Unable to load escalas: ' + error.message, 'type': 'danger'};
           });
    };
    
});