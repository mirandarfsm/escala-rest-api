app.controller("CadastroAfastamentoCtrl", function(AuthenticationService,userFactory,afastamentoFactory){
    var self = this;
    var user = AuthenticationService.getUsuario();
    getAfastamentos(user);
  
    self.novo = function(){
        self.afastamento = {};
        self.afastamento.usuario = user;
    };

    self.editar = function(index){
        self.afastamento = self.afastamentos[index];
		self.data_inicio = new Date(self.afastamento.data_inicio);
        self.data_fim = new Date(self.afastamento.data_fim);
    };
    
    self.cancelar = function(){
        self.afastamento = undefined; 
    };

    self.salvar = function(){
    	self.afastamento.data_inicio = new Date(self.data_inicio).getTime();
    	self.afastamento.data_fim = new Date(self.data_fim).getTime();
        //$filter('date')(new Date(user.data_promocao), 'yyyy-MM-dd');
    	if(self.afastamento.id){
    		self.atualizar(self.afastamento);
    	}else{
    		self.inserir(self.afastamento);
    	}
    };

	self.inserir = function(afastamento){
		afastamentoFactory.insert(afastamento).then(function(data){
    		getAfastamentos(user);
            self.afastamento = undefined; 
    	});
	};

	self.atualizar = function(afastamento){
		afastamentoFactory.update(afastamento).then(function(data){
    		self.afastamento = undefined; 
    	});	
	};

	self.deletar = function(index){
		var afastamento = self.afastamentos[index];
        afastamentosFactory.delete(afastamento.id).then(function(data){
            self.users.splice(index,1);
        });
	};

  	function getAfastamentos(user) {
        userFactory.getAfastamentos(user.id).success(function (data) {
            self.afastamentos = data.afastamentos;
        });
    };

});