(function() {
    'use strict';
    
    angular
        .module('Escalante')
        .directive('checkList',checkList);
                   
    function checkList() {
        var directive = {
            scope: {
                list: '=checkList',
                value: '='
            },
            link: link
        };
        
        return directive;
        
        function link(scope, elem, attrs) {
            var handler = function(setup) {
                var checked = elem.prop('checked');
                if (scope.list === undefined) scope.list = [];
                var index = scope.list.indexOf(scope.value);
                
                if (checked && index == -1) {
                    if (setup) elem.prop('checked', false);
                    else scope.list.push(scope.value);
                } else if (!checked && index != -1) {
                    if (setup) elem.prop('checked', true);
                    else scope.list.splice(index, 1);
                }
            }
        
            var setupHandler = handler.bind(null, true);
            var changeHandler = handler.bind(null, false);
            
            elem.bind('change', function() {
                scope.$apply(changeHandler);
            });
            scope.$watch('list', setupHandler, true);
        }
    }

})();