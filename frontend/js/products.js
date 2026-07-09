fetch("http://127.0.0.1:8000/products")
.then(response => response.json())
.then(products => {

    let table = document.getElementById("productTable");
    table.innerHTML = "";

    products.forEach(product => {

        table.innerHTML += `
        <tr>
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.description}</td>
            <td>₹${product.price}</td>
            <td>${product.stock}</td>
            <td>${product.category_id}</td>
            <td>${product.vendor_id}</td>
        </tr>
        `;

    });

})
.catch(error => {
    console.error(error);
    alert("Unable to load products.");
});