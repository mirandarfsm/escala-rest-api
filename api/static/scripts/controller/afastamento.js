app.controller("CadastroAfastamentoCtrl", function(AuthenticationService){
    var self = this;
    self.novoAfastamento = function(){
        self.afastamento = {};
        self.afastamento.usuario = AuthenticationService.getUsuario();
    }
    self.cancelar = function(){
        self.afastamento = undefined; 
    }
});