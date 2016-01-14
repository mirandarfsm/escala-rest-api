app.controller('CadastroEscalaCtrl', ['escalaFactory', function (escalaFactory) {
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

    self.closeAlert = function(){
        self.alert = undefined;
    };

    self.novaEscala = function(){
        self.escala = {};
    };

    self.editarEscala = function(index){
        self.escala = self.escalas[index];
    };

    self.cancelar = function(){
        self.escala = undefined;
    } ;

    self.adicionarFeriado = function(){
        if (!self.escala.feriados){
            self.escala.feriados = [];
        }
        self.escala.feriados.push(new Date);
    };

   self.adicionarRoxa = function(){
        if (!self.escala.roxas){
            self.escala.roxas = [];
        }
        self.escala.roxas.push(new Date);
    };

    self.removerFeriado = function(index){
        self.escala.feriados.splice(index,1);
    };

    self.removerRoxa = function(index){
        self.escala.roxas.splice(index,1);
    };

    self.salvarEscala = function(escala){
      console.log(escala);
      //escala.data_promocao = $filter('date')(new Date(user.data_promocao), 'yyyy-MM-dd');
      if(escala['id']){
        self.atualizarEscala(escala);
      }else{
        self.inserirEscala(escala);
      }
    };
/*
    self.salvarEscala = function(user){
        user.data_promocao = $filter('date')(new Date(user.data_promocao), 'yyyy-MM-dd');
        if(user['id']){
            $scope.updateUser(user);
        }else{
            $scope.insertUser(user);
        }
    };
*/
    self.atualizarEscala = function (object) {
       escalaFactory.updateEscala(object)
          .success(function () {
              self.alert = {'msg':'Updated Escala! Refreshing user list.', 'type': 'success'};
              self.escala = undefined 
          })
          .error(function (error) {
              self.alert = { 'msg':'Unable to update escala: ' + error.message, 'type': 'danger'};
          });
    };

    self.inserirEscala = function (escala) {
        escalaFactory.insertEscala(escala)
            .success(function () {
                getEscala();
                self.alert = {'msg':'Inserted Escala! Refreshing user list.','type':'success'};
                self.escala = undefined           
            }).
            error(function(error) {
                self.alert = {'msg':'Unable to insert escala: ' + error.message, 'type': 'danger'};
            });
    };

    self.deletarEscala = function (index) {
        var escala = self.escalas[index]
        escalaFactory.deleteEscala(escala.id)
        .success(function () {
            self.alert = {'msg':'Deleted User! Refreshing escala list.', 'type': 'success'};   
            self.escalas.splice(index,1);
            //$scope.orders = null;
        })
        .error(function (error) {
            self.alert = { 'msg':'Unable to delete escala: ' + error.message, 'type': 'danger'};
        });
    };


}]);

app.controller('AssociacaoEscalaCtrl', ['escalaFactory','userFactory', function (escalaFactory,userFactory) {
    var self = this;
    getEscala();
    getUsers();
    function getEscala(){
        escalaFactory.getEscalas()
            .success(function (data, status, headers, config) {
                self.escalas = data.escalas;
            })
            .error(function (error) {
                self.alert = {'msg':'Unable to load escalas: ' + error.message, 'type': 'danger'};
            });
    };
    
    self.editarEscala = function(index){
        self.escala = self.escalas[index];
        escalaFactory.getUsuarios(self.escala.id)
            .success(function (data, status, headers, config) {
                self.escala.usuarios = data.usuarios;
            })
            .error(function (error) {
                self.alert = {'msg':'Unable to load user: ' + error.message, 'type': 'danger'};
            });
    };
    
    function getUsers() {
        userFactory.getUsers()
            .success(function (data, status, headers, config) {
                self.usuarios = data.usuarios;
            })
            .error(function (error) {
                self.alert = {'msg':'Unable to load user: ' + error.message, 'type': 'danger'};
            });
    };
    
    self.cancelar = function(){
        self.escala = undefined;
    } ;
    
    self.adicionarUsuario = function(usuario){
        self.escala.usuarios = usuario;
    };
    self.salvar = function(escala){
        //console.log(escala);
        self.atualizarEscala(escala);
    }
    self.atualizarEscala = function (object) {
       escalaFactory.updateEscala(object)
          .success(function () {
              self.alert = {'msg':'Updated Escala! Refreshing user list.', 'type': 'success'};
              self.escala = undefined 
          })
          .error(function (error) {
              self.alert = { 'msg':'Unable to update escala: ' + error.message, 'type': 'danger'};
          });
    };
}]);
