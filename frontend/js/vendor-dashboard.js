console.log("HELLO FROM VENDOR DASHBOARD");
const vendorId = localStorage.getItem("vendorId");
loadVendorNotifications();
// Load Dashboard Details
fetch(`http://localhost:8000/vendors/${vendorId}/dashboard`)
.then(response => response.json())
.then(data => {
    document.getElementById("vendorId").innerText =
    data.vendor_id;

    document.getElementById("ownerName").innerText = data.owner_name;
    document.getElementById("businessName").innerText = data.business_name;
    document.getElementById("email").innerText = data.email;
    document.getElementById("phone").innerText = data.phone;
    document.getElementById("status").innerText = data.status;
    document.getElementById("products").innerText = data.total_products;
    document.getElementById("inventory").innerText = data.total_inventory;
    document.getElementById("vendorRevenue").innerText =
    "₹" + data.total_revenue;

document.getElementById("vendorOrders").innerText =
    data.completed_orders;

document.getElementById("bestProduct").innerText =
    data.best_product;

document.getElementById("inventoryValue").innerText =
    "₹" + data.inventory_value;
document.getElementById("inventoryValue").innerText =
"₹" + data.inventory_value;


// ====================
// Sales Chart
// ====================

new Chart(document.getElementById("salesChart"),{

    type:"line",

    data:{
        labels:["Jan","Feb","Mar","Apr","May","Jun"],

        datasets:[{
            label:"Revenue",

            data:[
                120000,
                180000,
                250000,
                320000,
                450000,
                data.total_revenue
            ],

            borderWidth:2,
            fill:false
        }]
    },

    options:{
        responsive:true,
        maintainAspectRatio:false
    }

});


// ====================
// Inventory Chart
// ====================

new Chart(document.getElementById("inventoryChart"),{

    type:"doughnut",

    data:{
        labels:["Inventory","Completed Orders"],

        datasets:[{

            data:[
                data.total_inventory,
                data.completed_orders
            ]

        }]
    },

    options:{
        responsive:true,
        maintainAspectRatio:false
    }

});



});

// Load Vendor Products
loadProducts();

function loadProducts(){

    fetch(`http://localhost:8000/products/vendor/${vendorId}`)
    .then(response => response.json())
    .then(products => {

        let table = document.getElementById("myProducts");

        table.innerHTML = "";

        products.forEach(product => {

            table.innerHTML += `
<tr>
    <td>${product.name}</td>
    <td>${product.description}</td>
    <td>₹${product.price}</td>
    <td>${product.stock}</td>
    <td>

    <button onclick="editProduct(${product.id}, '${product.name}', '${product.description}', ${product.price}, ${product.stock}, ${product.category_id})">
        ✏️ Edit
    </button>

    <button onclick="deleteProduct(${product.id})">
        🗑️ Delete
    </button>

</td>
</tr>
`;

        });

    });

}

// Add Product
function addProduct(){

    const name = document.getElementById("productName").value;
    const description = document.getElementById("description").value;
    const price = parseFloat(document.getElementById("price").value);
    const stock = parseInt(document.getElementById("stock").value);
    const category_id = parseInt(document.getElementById("categoryId").value);

    if(
        name==="" ||
        description==="" ||
        isNaN(price) ||
        isNaN(stock) ||
        isNaN(category_id)
    ){

        alert("Please fill all fields.");

        return;

    }

    fetch("http://localhost:8000/products/add",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            name:name,
            description:description,
            price:price,
            stock:stock,
            category_id:category_id,
            vendor_id:parseInt(vendorId)

        })

    })

    .then(response=>response.json())

    .then(data => {

        alert("Product Added Successfully!");

        cancelProductForm();

        location.reload();

});

}
function showForm(){

    document.getElementById("productForm").style.display = "block";

}
function cancelProductForm() {
    document.getElementById("productForm").style.display = "none";

    document.getElementById("productName").value = "";
    document.getElementById("description").value = "";
    document.getElementById("price").value = "";
    document.getElementById("stock").value = "";
    document.getElementById("categoryId").value = "";
}
function cancelProductForm() {

    document.getElementById("productForm").style.display = "none";

    document.getElementById("productName").value = "";
    document.getElementById("description").value = "";
    document.getElementById("price").value = "";
    document.getElementById("stock").value = "";
    document.getElementById("categoryId").value = "";

}

// Add this new function
function editProduct(productId, name, description, price, stock, categoryId){

    const newName = prompt("Product Name:", name);
    if(newName === null) return;

    const newDescription = prompt("Description:", description);
    if(newDescription === null) return;

    const newPrice = prompt("Price:", price);
    if(newPrice === null) return;

    const newStock = prompt("Stock:", stock);
    if(newStock === null) return;

    fetch(`http://localhost:8000/products/update/${productId}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: newName,
            description: newDescription,
            price: parseFloat(newPrice),
            stock: parseInt(newStock),
            category_id: categoryId,
            vendor_id: parseInt(vendorId)

        })

    })

    .then(response => response.json())

    .then(data => {

        alert("Product Updated Successfully!");

        location.reload();

    });

}
function deleteProduct(productId){

    const confirmDelete = confirm("Are you sure you want to delete this product?");

    if(!confirmDelete){
        return;
    }

    fetch(`http://localhost:8000/products/delete/${productId}`,{

        method:"DELETE"

    })

    .then(response=>response.json())

    .then(data=>{

        alert("Product Deleted Successfully!");

        location.reload();

    });

}
// Logout
function logout(){

    localStorage.clear();

    window.location.href="index.html";

}
// Logout
function logout(){

    localStorage.clear();

    window.location.href="index.html";

}
function loadVendorNotifications(){

    fetch(
        `http://localhost:8000/notifications/vendor/${vendorId}`
    )

    .then(response => response.json())

    .then(notifications => {

        const list =
            document.getElementById(
                "vendorNotificationList"
            );

        const count =
            document.getElementById(
                "vendorNotificationCount"
            );

        count.innerText =
            notifications.length;

        list.innerHTML = "";

        if(notifications.length === 0){

            list.innerHTML =
                "<p>No notifications</p>";

            return;
        }

        notifications.forEach(notification => {

            list.innerHTML += `

                <div class="notification-item">

                    <p>
                        ${notification.message}
                    </p>

                    <small>
                        ${notification.created_at}
                    </small>

                </div>

            `;

        });

    });

}


function toggleVendorNotifications(){

    const panel =
        document.getElementById(
            "vendorNotificationPanel"
        );

    if(panel.style.display === "block"){

        panel.style.display = "none";

    }
    else{

        panel.style.display = "block";

    }

}
