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