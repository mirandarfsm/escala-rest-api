(function(){
	'use strict';

	angular
		.module('Escalante')
		.factory('autenticacaoService',autenticacaoService);

	autenticacaoService.$inject = ['Restangular','$http','$rootScope','$timeout'];

	function autenticacaoService(Restangular,$http,$rootScope,$timeout){

		var usuario = undefined;

		var service = {
			get: get,
			login: login,
			getUsuario: getUsuario,
			getToken: getToken,
			logout: logout,
			isLogged: isLogged,
			isAdmin: isAdmin,
			isEscalante: isEscalante
			
		};

		function login(username, password) {
	    	var headers = {Authorization: "Basic " + btoa(username + ":" + password)};
	    	return $http.get('/auth/request-token', {headers : headers}).success(function(data){
		        usuario = data.usuario;
		        usuario.token = data.token;
		        $rootScope.usuario = usuario;
		        $timeout(logout, 3600000);
		        return usuario;
		      });
	  	}

		function get(){
			return Restangular.service('usuarios').one('me');
		}

		function getUsuario(){
	    	return usuario;
	  	}

		function getToken(){
			return usuario.token;
		}

		function logout(){
			usuario = undefined;
			$rootScope.usuario = undefined; 
		}

		function isLogged(){
			return !!usuario;
		}

		function isAdmin(){
			if(service.isLogged()){
			  return checkPerfil(usuario.perfis,0);
			}
			return false;
		}
		
		function isEscalante(){
			if(service.isLogged()){
			  return checkPerfil(usuario.perfis,1);
			}
			return false;
		}
		
		function checkPerfil(arr, val) {
			return arr.some(function(arrVal) {
				return val === arrVal;
			});
		}

		return service;
	}

})();