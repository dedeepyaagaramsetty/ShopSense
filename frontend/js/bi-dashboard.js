fetch("http://127.0.0.1:8000/analytics/revenue-analysis")

.then(res=>res.json())

.then(data=>{

document.getElementById("revenue").innerText=
"₹"+data.current_month_revenue;

document.getElementById("orders").innerText=
data.completed_orders;

document.getElementById("gmv").innerText=
"₹"+data.gmv;

document.getElementById("growth").innerText=
data.growth_percentage+"%";

new Chart(document.getElementById("revenueChart"),{

type:"bar",

data:{

labels:["Current Month","Last Month"],

datasets:[{

label:"Revenue",

data:[
data.current_month_revenue,
data.last_month_revenue
]

}]

},

options:{

responsive:true,

maintainAspectRatio:false

}

});

});
fetch("http://127.0.0.1:8000/analytics/marketplace")

.then(res=>res.json())

.then(data=>{

new Chart(document.getElementById("marketChart"),{

type:"pie",

data:{

labels:[
"Customers",
"Vendors",
"Products",
"Orders"
],

datasets:[{

data:[
data.customers,
data.vendors,
data.products,
data.orders
]

}]

},

options:{

responsive:true,

maintainAspectRatio:false

}

});

});