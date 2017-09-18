(function() {
    'use strict';

    angular.module('money.config')
        .config(config)

    config.$inject = ['$locationProvider'];

    function config($locationProvider) {
        $locationProvider.html5Mode(true);
    }
})();