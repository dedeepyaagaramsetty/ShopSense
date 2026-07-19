const customerId = localStorage.getItem("customerId");

fetch(`http://127.0.0.1:8000/customers/${customerId}/orders`)
.then(response => response.json())
.then(data => {

    const table = document.getElementById("ordersTable");

    table.innerHTML = "";

    data.forEach(order => {

        table.innerHTML += `

        <tr>

            <td>${order.order_id}</td>

            <td>${order.product}</td>

            <td>${order.quantity}</td>

            <td>₹${order.amount}</td>

            <td>${order.status}</td>

            <td>${order.date}</td>

        </tr>

        `;

    });

});

function logout(){

    localStorage.clear();

    window.location.href = "index.html";

}