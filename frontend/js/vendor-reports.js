const vendorId = localStorage.getItem("vendorId");

fetch(`http://localhost:8000/vendors/${vendorId}/reports`)
.then(response => response.json())
.then(data => {

    document.getElementById("revenue").innerText =
        "₹" + data.total_revenue;

    document.getElementById("productsSold").innerText =
        data.products_sold;

    document.getElementById("completedOrders").innerText =
        data.completed_orders;

    document.getElementById("pendingOrders").innerText =
        data.pending_orders;

});