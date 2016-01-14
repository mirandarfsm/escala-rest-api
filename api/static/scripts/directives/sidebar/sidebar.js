app.directive("sidebar",function(){
	return {
        templateUrl:'scripts/directives/sidebar/sidebar.html',
        restrict: 'E',
        controller: "SidebarCtrl as sidebarCtrl"
    	};
});

app.controller('SidebarCtrl',function(){
});