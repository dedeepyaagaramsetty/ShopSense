// Dashboard Statistics

fetch("http://127.0.0.1:8000/admin/dashboard")
.then(response => response.json())
.then(data => {

    document.getElementById("totalVendors").innerText = data.total_vendors;

    document.getElementById("approvedVendors").innerText = data.approved_vendors;

    document.getElementById("pendingVendors").innerText = data.pending_vendors;

    document.getElementById("suspendedVendors").innerText = data.suspended_vendors;

    document.getElementById("totalProducts").innerText = data.total_products;

    document.getElementById("lowStockProducts").innerText = data.low_stock_products;

})
.catch(error => console.log(error));


// Marketplace Reports

fetch("http://127.0.0.1:8000/admin/reports")
.then(response => response.json())
.then(data => {

    document.getElementById("totalOrders").innerText = data.total_orders;

    document.getElementById("totalRevenue").innerText = data.total_revenue;

    document.getElementById("bestProduct").innerText = data.best_selling_product;

})
.catch(error => console.log(error));
// ============================
// Analytics
// ============================

fetch("http://127.0.0.1:8000/admin/analytics")
.then(response => response.json())
.then(data => {

    document.getElementById("totalCustomers").innerText =
    data.total_customers;

    new Chart(

    document.getElementById("analyticsChart"),

    {

        type: "bar",

        data: {

            labels: [

                "Customers",

                "Vendors",

                "Products"

            ],

            datasets: [

                {

                    label: "Total Count",

                    data: [

                        data.total_customers,

                        data.total_vendors,

                        data.total_products

                    ]

                }

            ]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false

        }

    }

);

    new Chart(

    document.getElementById("ordersChart"),

    {

        type: "pie",

        data: {

            labels: [

                "Completed",

                "Pending"

            ],

            datasets: [

                {

                    data: [

                        data.completed_orders,

                        data.pending_orders

                    ]

                }

            ]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false

        }

    }

);

});