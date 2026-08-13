// ==========================================
// ShopSense Business Intelligence Dashboard
// ==========================================


// ==========================================
// 1. REVENUE ANALYSIS
// ==========================================

fetch("http://localhost:8000/analytics/revenue-analysis")

.then(res => res.json())

.then(data => {

    document.getElementById("revenue").innerText =
        "₹" + Number(data.current_month_revenue).toLocaleString("en-IN");

    document.getElementById("orders").innerText =
        Number(data.completed_orders).toLocaleString("en-IN");

    document.getElementById("gmv").innerText =
        "₹" + Number(data.gmv).toLocaleString("en-IN");

    document.getElementById("growth").innerText =
        Number(data.growth_percentage).toFixed(2) + "%";


    new Chart(document.getElementById("revenueChart"), {

        type: "bar",

        data: {

            labels: [
                "Current Month",
                "Last Month"
            ],

            datasets: [{

                label: "Revenue (₹)",

                data: [
                    data.current_month_revenue,
                    data.last_month_revenue
                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

})

.catch(error => {

    console.error("Revenue API Error:", error);

});


// ==========================================
// 2. MARKETPLACE OVERVIEW
// ==========================================

fetch("http://localhost:8000/analytics/marketplace")

.then(res => res.json())

.then(data => {

    new Chart(document.getElementById("marketChart"), {

        type: "pie",

        data: {

            labels: [
                "Customers",
                "Vendors",
                "Products",
                "Orders"
            ],

            datasets: [{

                data: [
                    data.customers,
                    data.vendors,
                    data.products,
                    data.orders
                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

})

.catch(error => {

    console.error("Marketplace API Error:", error);

});


// ==========================================
// 3. VENDOR PERFORMANCE
// ==========================================

fetch("http://localhost:8000/analytics/vendor-performance")

.then(res => res.json())

.then(data => {

    const vendorNames =
        data.map(vendor => vendor.business_name);

    const vendorRevenue =
        data.map(vendor => vendor.revenue);


    new Chart(document.getElementById("vendorChart"), {

        type: "bar",

        data: {

            labels: vendorNames,

            datasets: [{

                label: "Revenue (₹)",

                data: vendorRevenue

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: true

                }

            },

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

})

.catch(error => {

    console.error("Vendor Performance API Error:", error);

});


// ==========================================
// 4. CUSTOMER & ORDER INSIGHTS
// ==========================================

fetch("http://localhost:8000/analytics/customer-insights")

.then(res => res.json())

.then(data => {

    new Chart(document.getElementById("customerChart"), {

        type: "doughnut",

        data: {

            labels: [
                "Completed Orders",
                "Pending Orders"
            ],

            datasets: [{

                data: [
                    data.completed_orders,
                    data.pending_orders
                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });


    console.log("Customer Insights:", data);

})

.catch(error => {

    console.error("Customer Insights API Error:", error);

});