app.controller("CadastroServicoCtrl", function(escalaFactory){
    var self = this;
    getEscala();
    function getEscala(){
        escalaFactory.getEscalas().success(function (data) {
            self.escalas = data.escalas;
        });
    };
    
    self.gerar = function(){
        escalaFactory.generateServices(self.escala.id).success(function(data, status, headers, config){
            console.log(data);
            console.log(status);
            console.log(headers);
            console.log(config);
        }).error(function(error){
            console.log(error);
        });
    };
    
    self.cancelar = function(){
        self.escala = {}
        self.data_inicio = "";
        self.data_fim = undefined;
    }
    
});

app.controller("TrocaServicoCtrl",function(AuthenticationService,userFactory){
    var self = this;
    var usuario = AuthenticationService.getUsuario();
    getServicos(usuario);
    
    self.tipos = ['','Preta','Vermelha','Roxa'];
    
    function getServicos(usuario){
        userFactory.getServicos(usuario.id).success(function (data) {
               self.servicos = data.servicos;
           }).error(function (error) {
               console.log(error);
           });
    };
});

app.controller("ServicosCrtl",function(servicoFactory){
    var self = this;
    
    getServicos();
    
    self.tipos = ["",'Preta','Vermelha','Roxa'];
    
    function getServicos(){
        servicoFactory.getAll().success(function (data) {
                console.log(data);
                self.servicos = data.servicos;
           }).error(function (error) {
               console.log(error);
           });
    };
});