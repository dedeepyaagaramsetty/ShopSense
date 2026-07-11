const vendorId = localStorage.getItem("vendorId");

fetch(`http://127.0.0.1:8000/vendors/${vendorId}/reports`)
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