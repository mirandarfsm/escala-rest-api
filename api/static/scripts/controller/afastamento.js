app.controller("CadastroAfastamentoCtrl", function(usuarioFactory){
    var self = this;
    getAfastamentos();

	self.deletar = function(index){
		var afastamento = self.afastamentos[index];
        usuarioFactory.deleteAfastamento(afastamento.id).then(function(data){
            self.afastamentos.splice(index,1);
        });
	};

  	function getAfastamentos(user) {
        usuarioFactory.getAfastamentos().success(function (data) {
            self.afastamentos = data.objects;
        });
    };

});

app.controller("CadastroAfastamentoNewCtrl", function($location,AuthenticationService,usuarioFactory){
    var self = this;
    var user = AuthenticationService.getUsuario();
    self.afastamento = {};
    self.afastamento.usuario = user
    
    self.salvar = function(){
        self.afastamento.data_inicio = new Date(self.data_inicio).getTime();
    	self.afastamento.data_fim = new Date(self.data_fim).getTime();
		usuarioFactory.insertAfastamento(self.afastamento).success(function() {
            $location.path("/cadastro-afastamento");
        });
	};
    
});

app.controller("CadastroAfastamentoDetailCtrl", function($routeParams,$location,usuarioFactory){
    var self = this;
    var id = $routeParams.id;
    
    usuarioFactory.getAfastamentosDetail(id).success(function(data){
        console.log(data);
        self.afastamento =  data;
        self.data_inicio = new Date(self.afastamento.data_inicio);
        self.data_fim = new Date(self.afastamento.data_fim);
    });
    
    self.salvar = function(){
        self.afastamento.data_inicio = new Date(self.data_inicio).getTime();
    	self.afastamento.data_fim = new Date(self.data_fim).getTime();
		usuarioFactory.updateAfastamento(self.afastamento).success(function(){
            $location.path("/cadastro-afastamento");
    	});	
	};
});

app.controller("GerenciaAfastamentoCtrl", function(afastamentoFactory){
    var self = this;
    getAfastamentos();

    self.deletar = function(index){
        var afastamento = self.afastamentos[index];
        afastamentoFactory.delete(afastamento.id).then(function(data){
            self.afastamentos.splice(index,1);
        });
    };

    function getAfastamentos(user) {
        afastamentoFactory.getAll().success(function (data) {
            self.afastamentos = data.objects;
        });
    };

});

app.controller("GerenciaAfastamentoDetailCtrl", function($routeParams,$location,afastamentoFactory){
    var self = this;
    var id = $routeParams.id;
    
    afastamentoFactory.get(id).success(function(data){
        self.afastamento =  data;
        self.data_inicio = new Date(self.afastamento.data_inicio);
        self.data_fim = new Date(self.afastamento.data_fim);
    });
    
    self.salvar = function(){
        self.afastamento.data_inicio = new Date(self.data_inicio).getTime();
        self.afastamento.data_fim = new Date(self.data_fim).getTime();
        usuarioFactory.updateAfastamento(self.afastamento).success(function(){
            $location.path("/gerencia-afastamento");
        }); 
    };

});
