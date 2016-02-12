app.controller("CadastroAfastamentoCtrl", function(AuthenticationService,userFactory,afastamentoFactory){
    var self = this;
    var user = AuthenticationService.getUsuario();
    getAfastamentos(user);

	self.deletar = function(index){
		var afastamento = self.afastamentos[index];
        afastamentoFactory.delete(afastamento.id).then(function(data){
            self.afastamentos.splice(index,1);
        });
	};

  	function getAfastamentos(user) {
        userFactory.getAfastamentos(user.id).success(function (data) {
            self.afastamentos = data.objects;
        });
    };

});

app.controller("CadastroAfastamentoNewCtrl", function($location,AuthenticationService,afastamentoFactory){
    var self = this;
    var user = AuthenticationService.getUsuario();
    self.afastamento = {};
    self.afastamento.usuario = user;
    
    self.salvar = function(){
        self.afastamento.data_inicio = new Date(self.data_inicio).getTime();
    	self.afastamento.data_fim = new Date(self.data_fim).getTime();
		afastamentoFactory.insert(self.afastamento).success(function() {
            $location.path("/cadastro-afastamento");
        });
	};
    
});

app.controller("CadastroAfastamentoDetailCtrl", function($routeParams,$location,afastamentoFactory){
    var self = this;
    var id = $routeParams.id;
    
    afastamentoFactory.get(id).success(function(data){
        console.log(data);
        self.afastamento =  data;
        self.data_inicio = new Date(self.afastamento.data_inicio);
        self.data_fim = new Date(self.afastamento.data_fim);
    });
    
    self.salvar = function(){
        self.afastamento.data_inicio = new Date(self.data_inicio).getTime();
    	self.afastamento.data_fim = new Date(self.data_fim).getTime();
		afastamentoFactory.update(self.afastamento).success(function(){
            $location.path("/cadastro-afastamento");
    	});	
	};
});