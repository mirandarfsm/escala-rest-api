app.controller('CadastroEscalaCtrl', function (escalaFactory,userFactory) {
    var self = this;

    getEscalas();
    getUsuarios();

    self.novo = function(){
        self.escala = {};
    };

    self.editar = function(index){
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

    self.salvar = function(){
      if(self.escala.id){
        self.atualizar(self.escala);
      }else{
        self.inserir(self.escala);
      }
    };

    self.inserir = function (escala) {
        escalaFactory.insertEscala(escala).success(function () {
            getEscalas();
            self.escala = undefined           
        });
    };

    self.atualizar = function (escala) {
       escalaFactory.updateEscala(escala).success(function () {
              self.escala = undefined 
          });
    };

    self.deletar = function (index) {
        var escala = self.escalas[index]
        escalaFactory.deleteEscala(escala.id).success(function () {
            self.escalas.splice(index,1);
        });
    };

    function getUsuarios() {
        userFactory.getAll().success(function (data) {
            self.usuarios = data.usuarios;
        });
    };

    function getEscalas(){
        escalaFactory.getEscalas().success(function (data) {
            self.escalas = data.escalas;
        });
    };

});