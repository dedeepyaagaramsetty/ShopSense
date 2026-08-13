const customerId = localStorage.getItem("customerId");

loadDashboard();
loadProducts();
loadRecommendations();
loadNotifications();
function loadDashboard() {

    fetch(`http://localhost:8000/customers/${customerId}/dashboard`)
    .then(response => response.json())
    .then(data => {
        

document.getElementById("customerName").innerText = data.full_name;
        document.getElementById("customerName").innerText =
            data.full_name;

        document.getElementById("customerEmail").innerText =
            data.email;

        document.getElementById("totalOrders").innerText =
            data.total_orders;

        document.getElementById("completedOrders").innerText =
            data.completed_orders;

        document.getElementById("pendingOrders").innerText =
            data.pending_orders;

        document.getElementById("totalSpent").innerText =
            "₹" + data.total_spent;

        document.getElementById("averageSpent").innerText =
            "₹" + data.average_spent;
        console.log("Dashboard values assigned successfully");


        // ======================
        // Order Status Chart
        // ======================

        new Chart(
            document.getElementById("customerOrdersChart"),
            {
                type: "pie",

                data: {
                    labels: [
                        "Completed",
                        "Pending"
                    ],

                    datasets: [{
                        data: [
                            data.completed_orders,
                            data.pending_orders
                        ]
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            }
        );


        // ======================
        // Spending Chart
        // ======================

        new Chart(
            document.getElementById("customerSpendChart"),
            {
                type: "bar",

                data: {
                    labels: [
                        "Total Spent",
                        "Average Order"
                    ],

                    datasets: [{
                        label: "Amount (₹)",

                        data: [
                            data.total_spent,
                            data.average_spent
                        ]
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            }
        );

    });

}
let allProducts = [];

function loadProducts() {

    fetch("http://localhost:8000/products/")
    .then(response => response.json())
    .then(products => {

        allProducts = products;

        displayProducts(products);

    })
    .catch(error => console.log(error));

}

function displayProducts(products){

    const container = document.getElementById("productsContainer");

    container.innerHTML = "";

    products.forEach(product=>{

        container.innerHTML += `

<div class="product-card">

    <div class="product-icon">

        📦

    </div>

    <h3>${product.name}</h3>

    <p>${product.description}</p>

    <h2>₹${product.price}</h2>

    <p>Stock: ${product.stock}</p>

    <button onclick='showBuyPopup(${product.id}, ${JSON.stringify(product.name)}, ${product.price})'>
        🛒 Buy Now
    </button>
    <button onclick="addToWishlist(${product.id})">
        ❤️ Wishlist
    </button>

</div>

`;



    });

}

function filterProducts(){
    console.log("Filter function called");

    let filtered = [...allProducts];

    const keyword =
    document.getElementById("searchBox").value.toLowerCase();

    const category =
    document.getElementById("categoryFilter").value;

    const sort =
    document.getElementById("sortFilter").value;

    // Search
    if(keyword !== ""){

        filtered = filtered.filter(product =>

            product.name.toLowerCase().includes(keyword)

        );

    }

    // Category

    if(category !== "All"){

        // Category Filter

if(category === "Electronics"){

    filtered = filtered.filter(product =>

        product.category_id === 1

    );

}

else if(category === "Mobiles"){

    filtered = filtered.filter(product =>

        product.category_id === 2

    );

}

else if(category === "Laptops"){

    filtered = filtered.filter(product =>

        product.category_id === 3

    );

}

else if(category === "Fashion"){

    filtered = filtered.filter(product =>

        product.category_id === 4

    );

}

else if(category === "Grocery"){

    filtered = filtered.filter(product =>

        product.category_id === 5

    );

}

    }

    // Sorting

    if(sort === "low"){

        filtered.sort((a,b)=>a.price-b.price);

    }

    if(sort === "high"){

        filtered.sort((a,b)=>b.price-a.price);

    }

    displayProducts(filtered);

}
let selectedProductId = null;

function showBuyPopup(productId,name,price){
    console.log("Popup Opened");


    selectedProductId = productId;

    document.getElementById("popupProduct").innerText =
        "Product : " + name;

    document.getElementById("popupPrice").innerText =
        "Price : ₹" + price;

    document.getElementById("buyPopup").style.display="flex";

}
function confirmPurchase(){

    const address = prompt(
        "Enter delivery address:",
        ""
    );

    if(!address){
        alert("Address is required.");
        return;
    }

    const paymentMethod = prompt(
        "Choose payment method:\n\nEnter UPI to continue:"
    );

    if(!paymentMethod){
        return;
    }

    if(paymentMethod.toUpperCase() !== "UPI"){

        alert("Currently only UPI payment is available.");

        return;
    }

    // Dummy UPI payment
    alert("💳 UPI Payment Successful!");

    fetch(
        `http://localhost:8000/customers/${customerId}/buy/${selectedProductId}`,
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                quantity: 1,

                address: address,

                payment_method: "UPI"

            })

        }
    )

    .then(async response => {

        const data = await response.json();

        if(!response.ok){

            throw new Error(
                data.detail || "Purchase failed"
            );

        }

        return data;

    })

    .then(data => {

        alert(
            "✅ Payment Successful!\n\n" +
            "📦 Order placed successfully!\n\n" +
            "Product: " + data.product +
            "\nQuantity: " + data.quantity +
            "\nAmount: ₹" + data.amount +
            "\nPayment: " + data.payment_method
        );

        closePopup();

        loadDashboard();

        loadProducts();

        loadRecommendations();

    })

    .catch(error => {

        alert("❌ " + error.message);

    });

}
function closePopup(){

    document.getElementById("buyPopup").style.display="none";

}



function logout(){

    localStorage.clear();

    window.location.href="index.html";

}
function addToWishlist(productId){

    fetch(`http://localhost:8000/customers/${customerId}/wishlist/${productId}`,{

        method:"POST"

    })

    .then(async response=>{

        const data = await response.json();

        if(!response.ok){

            throw new Error(data.detail);

        }

        return data;

    })

    .then(data=>{

        alert(data.message);

    })

    .catch(error=>{

        alert(error.message);

    });

}
function loadRecommendations(){

    fetch(`http://localhost:8000/customers/${customerId}/recommendations`)

    .then(response => response.json())

    .then(products=>{

        const container =
        document.getElementById("recommendationContainer");

        container.innerHTML = "";

        products.forEach(product=>{

            let icon = "📦";

            if(product.category_id === 1) icon = "📺";
            if(product.category_id === 2) icon = "📱";
            if(product.category_id === 3) icon = "💻";
            if(product.category_id === 4) icon = "👕";
            if(product.category_id === 5) icon = "🛒";

            container.innerHTML += `

<div class="product-card">

    <div style="
        background:#FFD54F;
        color:black;
        display:inline-block;
        padding:4px 10px;
        border-radius:20px;
        font-size:12px;
        font-weight:bold;
        margin-bottom:10px;
    ">
        ⭐ Recommended
    </div>

    <div class="product-icon">
        ${icon}
    </div>

    <h3>${product.name}</h3>

    <p>${product.description}</p>

    <h2>₹${product.price}</h2>

   <button onclick="showBuyPopup(${product.id}, '${product.name}', ${product.price})">
    🛒 Buy Now
</button>
</div>

`;

        });

    });

}
function loadNotifications(){

    fetch(
        `http://localhost:8000/notifications/customer/${customerId}`
    )

    .then(response => response.json())

    .then(notifications => {

        const list =
            document.getElementById("notificationList");

        const count =
            document.getElementById("notificationCount");

        count.innerText = notifications.length;

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

    })

    .catch(error => {

        console.error(
            "Notification error:",
            error
        );

    });
}


function toggleNotifications(){

    const panel =
        document.getElementById(
            "notificationPanel"
        );

    if(panel.style.display === "block"){

        panel.style.display = "none";

    }
    else{

        panel.style.display = "block";

    }

}