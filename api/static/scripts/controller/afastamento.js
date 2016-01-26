app.controller("CadastroAfastamentoCtrl", function(AuthenticationService,userFactory,afastamentoFactory){
    var self = this;
    var user = AuthenticationService.getUsuario();
    getAfastamentos(user);
    
    self.novo = function(){
        self.afastamento = {};
        self.afastamento.usuario = user;
    }

    self.editar = function(index){
        self.afastamento = self.afastamentos[index];
    }
    
    self.cancelar = function(){
        self.afastamento = undefined; 
    }

    self.salvar = function(afastamento){
    	console.log(afastamento);
    	if(afastamento['id']){
    		self.atualizar(afastamento);
    	}else{
    		self.inserir(afastamento);
    	}
    };

	self.inserir = function(afastamento){
		afastamentoFactory.insert(afastamento).then(function(data){
    		console.log(data);
    		self.afastamento = undefined; 
    	});
	} 

	self.atualizar = function(afastamento){
		afastamentoFactory.update(afastamento).then(function(data){
    		console.log(data);
    		self.afastamento = undefined; 
    	});	
	};

	self.deletar = function(index){
		var afastamento = self.afastamentos[index];
        afastamentosFactory.delete(afastamento.id).then(function(data){
        	console.log(data);
            self.users.splice(index,1);
        });
	}

    function getAfastamentos(user) {
        userFactory.getAfastamentos(user.id).then(function (data) {
            self.afastamentos = data.afastamentos;
        });
    };
});