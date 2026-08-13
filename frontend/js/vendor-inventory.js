const vendorId = localStorage.getItem("vendorId");

fetch(`http://localhost:8000/vendors/${vendorId}/inventory`)
.then(response => response.json())
.then(data => {

    document.getElementById("totalProducts").innerText =
        data.total_products;

    document.getElementById("totalStock").innerText =
        data.total_stock;

    document.getElementById("inventoryValue").innerText =
        "₹" + data.total_inventory_value;

    let table = document.getElementById("inventoryTable");

    table.innerHTML = "";

    data.products.forEach(product => {

        table.innerHTML += `
        <tr>
            <td>${product.name}</td>
            <td>₹${product.price}</td>
            <td>${product.stock}</td>
            <td>₹${product.inventory_value}</td>
        </tr>
        `;

    });

});