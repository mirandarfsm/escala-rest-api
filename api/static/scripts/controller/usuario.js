app.controller('CadastroUsuarioCtrl',function (userFactory) {
    var self = this;
    getUsuarios();

    self.deletar = function(index) {
        var usuario = self.usuarios[index]
        userFactory.delete(usuario.id).success(function () {
            self.usuarios.splice(index,1);
        });
    };

    function getUsuarios() {
        userFactory.getAll().success(function (data) {
            self.usuarios = data.objects;
        });
    };
});

app.controller('CadastroUsuarioDetailCtrl',function ($routeParams,userFactory,$location) {
    var self = this;
    var id = $routeParams.id;
    userFactory.get(id).success(function(data){
        self.usuario =  data;
        self.data_promocao = new Date(self.usuario.data_promocao);
    });
    
    self.salvar = function() {
        self.usuario.data_promocao = new Date(self.data_promocao).getTime();
        userFactory.update(self.usuario).success(function(){
            $location.path('/cadastro-usuario');
        });
    };
});

app.controller('CadastroUsuarioNewCtrl',function ($location,userFactory) {
    var self = this;
    
    self.salvar = function() {
        self.usuario.data_promocao = new Date(self.data_promocao).getTime();
        userFactory.insert(self.usuario).success(function() {
            $location.path('/cadastro-usuario');
        });
    };
});