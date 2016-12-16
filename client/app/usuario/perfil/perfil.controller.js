(function(){
	'use strict';
	
	angular
		.module('Escalante')
		.controller('PerfilUsuarioController',PerfilUsuarioController)
		.controller('TrocaSenhaModalController',TrocaSenhaModalController);
	
	PerfilUsuarioController.$inject = ['$uibModal'];
	TrocaSenhaModalController.$inject = ['$uibModalInstance'];
	
	function PerfilUsuarioController($uibModal){
		var vm = this;
		vm.show = show;
		
		function show() {
			var modalInstance = $uibModal.open({
				templateUrl: 'troca-senha-modal.html',
				controller: 'TrocaSenhaModalController',
				controllerAs: 'vm'
			});
		};		
	
	}
	
	function TrocaSenhaModalController($uibModalInstance) {
		var vm = this;
		
		vm.salvar = salvar;
		vm.cancel = cancel; 
			
		function salvar(){
			$uibModalInstance.dismiss('cancel');
		}
		
		function cancel() {
			$uibModalInstance.dismiss('cancel');
		};
	}

})();