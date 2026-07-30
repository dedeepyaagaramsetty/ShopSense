// Dashboard Statistics

fetch("http://127.0.0.1:8000/admin/dashboard")
.then(response => response.json())
.then(data => {

    animateValue("totalVendors",data.total_vendors);

    animateValue("approvedVendors",data.approved_vendors);

    animateValue("pendingVendors",data.pending_vendors);

    animateValue("suspendedVendors", data.suspended_vendors);

    animateValue("totalProducts", data.total_products);

    animateValue("lowStockProducts",data.low_stock_products);

})
.catch(error => console.log(error));


// Marketplace Reports

fetch("http://127.0.0.1:8000/admin/reports")
.then(response => response.json())
.then(data => {

    animateValue("totalOrders",data.total_orders);

    animateValue("totalRevenue",data.total_revenue);

    animateValue("bestProduct",data.best_selling_product);

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
function animateValue(id,end){

    let start=0;

    const duration=1000;

    const increment=end/50;

    const obj=document.getElementById(id);

    const timer=setInterval(()=>{

        start+=increment;

        if(start>=end){

            obj.innerText=end;

            clearInterval(timer);

        }

        else{

            obj.innerText=Math.floor(start);

        }

    },duration/50);

}
