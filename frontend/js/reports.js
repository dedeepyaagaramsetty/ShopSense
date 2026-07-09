fetch("http://127.0.0.1:8000/admin/reports")
.then(response => response.json())
.then(data => {

    document.getElementById("revenue").innerText =
        data.total_revenue;

    document.getElementById("orders").innerText =
        data.total_orders;

    document.getElementById("bestProduct").innerText =
        data.best_selling_product;

})
.catch(error => console.log(error));