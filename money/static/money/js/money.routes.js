(function () {
    'use strict';

    angular.module('money.routes')
        .config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        $routeProvider.when('/payment', {
            templateUrl : "/static/money/template/payment.html"
        }).otherwise('/');
    }
})();