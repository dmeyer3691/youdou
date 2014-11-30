(function() {
'use strict';

angular
  .module('YouDoU', [])
  .controller('AppController', AppController);

function AppController() {
  var vm = this;
  vm.view = 'profile';
}

})();
