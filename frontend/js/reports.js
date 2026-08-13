fetch("http://localhost:8000/admin/reports")
.then(response => response.json())
.then(data => {

    document.getElementById("revenue").innerText =
        data.total_revenue;

    document.getElementById("orders").innerText =
        data.total_orders;

    document.getElementById("bestProduct").innerText =
        data.best_selling_product;
    document.getElementById("completedOrders").innerText =
        data.completed_orders;

    document.getElementById("pendingOrders").innerText =
        data.pending_orders;

})
.catch(error => console.log(error));