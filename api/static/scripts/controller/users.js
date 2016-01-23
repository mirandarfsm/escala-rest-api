app.controller('CadastroUsuarioCtrl', ['$filter','userFactory', function ($filter,userFactory) {
    var self = this;
    
    getUsers();
    
    function getUsers() {
        userFactory.getUsers()
            .success(function (data, status, headers, config) {
                self.users = data.usuarios;
            })
            .error(function (error) {
                self.alert = {'msg':'Unable to load user: ' + error.message, 'type': 'danger'};
            });
    };

    self.closeAlert = function(){
        self.alert = undefined;
    };

    self.newUser = function(){
        self.user = {}
    };

    self.cancel = function(){
        self.user = undefined; 
    }

    self.editeUser = function(index){
        self.user = self.users[index];
        self.user.data_promocao = new Date(self.user.data_promocao)
    };

    self.saveUser = function(user){
        user.data_promocao = $filter('date')(new Date(user.data_promocao), 'yyyy-MM-dd');
        if(user['id']){
            self.updateUser(user);
        }else{
            self.insertUser(user);
        }
    };

    self.updateUser = function (user) {
        userFactory.updateUser(user)
          .success(function () {
              self.alert = {'msg':'Updated User! Refreshing user list.', 'type': 'success'};
              self.user = undefined 
          })
          .error(function (error) {
              self.alert = { 'msg':'Unable to update user: ' + error.message, 'type': 'danger'};
          });
    };

    self.insertUser = function (user) {
        userFactory.insertUser(user)
            .success(function () {
                getUsers();
                self.alert = {'msg':'Inserted User! Refreshing user list.','type':'success'};
                self.user = undefined           
            }).
            error(function(error) {
                self.alert = {'msg':'Unable to insert user: ' + error.message, 'type': 'danger'};
            });
    };

    self.deleteUser = function (index) {
        var user = self.users[index]
        userFactory.deleteUser(user.id)
        .success(function () {
            self.alert = {'msg':'Deleted User! Refreshing user list.', 'type': 'success'};   
            self.users.splice(index,1);
            //$scope.orders = null;
        })
        .error(function (error) {
            self.alert = { 'msg':'Unable to delete user: ' + error.message, 'type': 'danger'};
        });
    };

    /*$scope.getUserOrders = function (id) {
        userFactory.getOrders(id)
        .success(function (orders) {
            $scope.alert = 'Retrieved orders!';
            $scope.orders = orders;
        })
        .error(function (error) {
            $scope.alert = 'Error retrieving users! ' + error.message;
        });
    };*/
}]);
