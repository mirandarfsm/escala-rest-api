app.controller("CadastroTrocaServicoCtrl",function(AuthenticationService,usuarioFactory){
    var self = this;
    getTrocaServicos();
    getTrocaServicosPendentes();

    self.tipos = ['Preta','Vermelha','Roxa'];
    
    self.minhasTrocas = false;

    self.aceitar = function (index) {
        var trocaServico = self.trocaServicosPendentes[index]
        usuarioFactory.acceptTrocaServico(trocaServico.id).success(function () {
            self.trocaServicosPendentes.splice(index,1);
        });
    };

    self.deletar = function (index) {
        var trocaServico = self.trocaServicos[index]
        usuarioFactory.deleteTrocaServico(trocaServico.id).success(function () {
            self.trocaServicos.splice(index,1);
        });
    };

    function getTrocaServicos(){
        usuarioFactory.getTrocaServico().success(function (data) {
                self.trocaServicos = data.objects;
           }).error(function (error) {
               console.log(error);
           });
    };
    function getTrocaServicosPendentes(){
        usuarioFactory.getTrocaServicoPendentes().success(function (data) {
               self.trocaServicosPendentes = data.objects;
           }).error(function (error) {
               console.log(error);
           });
    };
});


app.controller("CadastroTrocaServicoNewCtrl",function($location,AuthenticationService,usuarioFactory){
    var self = this;
    var user = AuthenticationService.getUsuario();
    self.trocaServico = {};
    self.trocaServico.substituido = user
    getServicos();
    
    self.salvar = function() {
        console.log(self.trocaServico);
        usuarioFactory.insertTrocaServico(self.trocaServico).success(function() {
            $location.path('/cadastro-troca-servico');
        });
    };

    function getServicos(){
        usuarioFactory.getServicos().success(function(data){
            self.servicos = data.objects;
        });
    };

});

app.controller("CadastroTrocaServicoDetailCtrl",function(AuthenticationService,usuarioFactory){

});

