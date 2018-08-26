var mainTable = Vue.component('table-grid', {
    delimiters: ['[[', ']]'],
    props: {
        filterKey: String,
        selectedMonth: String,
        sortOrders: {}
    },
    template: '#main-table-template',
    data: function () {
        return {
            sortKey: '',
            columns: ['Categorie'],
            tableData: []
        }
    },
    computed: {
        filteredData: function () {
            var filterKey = this.filterKey && this.filterKey.toLowerCase();
            var data = this.tableData;
            if (filterKey) {
                data = data.filter(function (row) {
                    return Object.keys(row).some(function (key) {
                        return String(row[key]).toLowerCase().indexOf(filterKey) > -1
                    })
                })
            }
            return data
        },
        compute_total: function() {
            var data = this.tableData;

            total = [];
            for(var i=0; i<data.length; i++) {

            }
        }
    },
    watch: {
        selectedMonth: function(newVal, oldVal) {
            this.fetchData(newVal);
        }
    },
    methods: {
        fetchData: function (month) {
            var vm = this;

            if (vm.tableData.length > 0) {
                this.tableData = [];
                this.columns = ['Categorie'];
            }

            //array base 0
            var monthIndex = vm.getMonthIndex(month) + 1;

            //create request
            var requestAPI = 'api/money/total/?month=';
            for (var i = 2; i > -1; i--) {
                if (monthIndex - i > 0) {
                    if (requestAPI.substr(requestAPI.length -1 ) === "=") {
                        requestAPI = requestAPI + String(monthIndex - i);
                    }
                    else {
                        requestAPI = requestAPI + ',' +String(monthIndex - i);
                    }
                }
            }

            fetch(requestAPI)
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    for (var key in data) {
                        var month = vm.getMonthName(parseInt(key) - 1);
                        vm.columns.push(month);
                        for (var cat in data[key]) {
                            var monthData = vm.getCategorieData(cat);
                            if (monthData.length == 0) {
                                vm.tableData.push({ Categorie: cat, [month]: data[key][cat] });
                            }
                            else {
                                monthData[[month]] = data[key][cat];
                            }
                        }
                    }
                })
                .catch((err) => console.error(err));
        },
        getMonthName: function (monthIndex) {
            var months = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"];

            return months[monthIndex];
        },
        getMonthIndex: function (monthName) {
            var months = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"];

            return months.indexOf(monthName);
        },
        getCategorieData: function(categorie) {
            for(var i=0; i<this.tableData.length; i++) {
                if (this.tableData[i].Categorie === categorie) {
                    return this.tableData[i];
                }
            }

            return [];
        }
    },
    created: function () {
        this.fetchData(this.selectedMonth);
    }
});

var mainTable = new Vue({
    el: "#mainComponent",
    data: {
        searchQuery: '',
        selectedMonth: '',
        monthNames: ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
    },
    created: function () {
        var d = new Date();
        var n = d.getMonth();
        this.selectedMonth = this.monthNames[n];
    }
});