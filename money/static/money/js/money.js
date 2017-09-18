(function() {
    'use strict';

    angular
    .module('money', [
        'money.config',
        'money.routes'
    ]);

  angular
      .module('money.config',[]);

  angular
    .module('money.routes', ['ngRoute']);

  angular
  .module('money')
  .run(run);

    run.$inject = ['$http'];

    /**
    * @name run
    * @desc Update xsrf $http headers to align with Django's defaults
    */
    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();