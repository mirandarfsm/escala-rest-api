app.controller('CadastroUsuarioCtrl',function (userFactory) {
    var self = this;
    getUsuarios();

    self.novo = function(){
        self.usuario = {}
    };

    self.cancelar = function(){
        self.usuario = undefined; 
    }

    self.editar = function(index){
        self.usuario = self.usuarios[index];
        self.data_promocao = new Date(self.usuario.data_promocao)
    };

    self.salvar = function(){
        self.usuario.data_promocao = new Date(self.data_promocao).getTime(); 
        //$filter('date')(new Date(user.data_promocao), 'yyyy-MM-dd');
        console.log(self.usuario)
        if(self.usuario.id){
            self.atualizar(self.usuario);
        }else{
            self.inserir(self.usuario);
        }
    };

    self.atualizar = function(usuario) {
        userFactory.update(usuario).success(function() {
              self.usuario = undefined 
          });
    };

    self.inserir = function(usuario) {
        userFactory.insert(usuario).success(function() {
                getUsuarios();
                self.usuario = undefined           
            });
    };

    self.deletar = function(index) {
        var usuario = self.usuarios[index]
        userFactory.delete(usuario.id).success(function () {
            self.usuarios.splice(index,1);
        });
    };

    function getUsuarios() {
        userFactory.getAll().success(function (data) {
            console.log(data);
            self.usuarios = data.usuarios;
        }).error(function(error){
            console.log(error);
        });
    };
});
