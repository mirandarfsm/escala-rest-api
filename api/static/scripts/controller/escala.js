app.controller('CadastroEscalaCtrl', function (escalaFactory,userFactory) {
    var self = this;

    getEscalas();

    self.deletar = function (index) {
        var escala = self.escalas[index]
        escalaFactory.delete(escala.id).success(function () {
            self.escalas.splice(index,1);
        });
    };

    function getEscalas(){
        escalaFactory.getAll().success(function (data) {
            self.escalas = data.escalas;
        });
    };

});

app.controller('CadastroEscalaNewCtrl', function ($location,escalaFactory,userFactory) {
    var self = this;
    
    getUsuarios();
    
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
    
    self.salvar = function() {
        //self.usuario.data_promocao = new Date(self.data_promocao).getTime();
        escalaFactory.insert(self.escala).success(function() {
            $location.path('/cadastro-escala');
        });
    };
    
    function getUsuarios() {
        userFactory.getAll().success(function (data) {
            self.usuarios = data.objects;
        });
    };
    
});

app.controller('CadastroEscalaDetailCtrl', function ($routeParams,$location,escalaFactory,userFactory) {
    var self = this
    var id = $routeParams.id;
    
    getUsuarios();
    
    escalaFactory.get(id).success(function(data){
        console.log(data)
        self.escala =  data; 
    });
    
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
    
    self.salvar = function() {
        //self.usuario.data_promocao = new Date(self.data_promocao).getTime();
        escalaFactory.update(self.escala).success(function(){
            $location.path('/cadastro-escala');
        });
    };
    
     function getUsuarios() {
        userFactory.getAll().success(function (data) {
            self.usuarios = data.objects;
        });
    };
});