const customerId = localStorage.getItem("customerId");

loadDashboard();
loadProducts();
loadRecommendations();
function loadDashboard(){

    fetch(`http://127.0.0.1:8000/customers/${customerId}/dashboard`)

    .then(response => response.json())

    .then(data=>{
        

        document.getElementById("customerName").innerText =
        data.full_name;

        document.getElementById("customerEmail").innerText =
        data.email;

        document.getElementById("totalOrders").innerText =
        data.total_orders;

    });

}

let allProducts = [];

function loadProducts(){

    fetch("http://127.0.0.1:8000/products/")

    .then(response=>response.json())

    .then(products=>{

        allProducts = products;

        displayProducts(products);

    });

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

    <button onclick="buyNow(${product.id})">
        🛒 Buy
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

function buyNow(productId){

    fetch(`http://127.0.0.1:8000/customers/${customerId}/buy/${productId}`, {

        method: "POST"

    })

    .then(async response => {

        const data = await response.json();

        if(!response.ok){
            throw new Error(data.detail);
        }

        return data;

    })

    .then(data => {

        alert(data.message);

        // Reload products so updated stock is shown
        loadProducts();

    })

    .catch(error => {

        alert(error.message);

    });

}

function logout(){

    localStorage.clear();

    window.location.href="index.html";

}
function addToWishlist(productId){

    fetch(`http://127.0.0.1:8000/customers/${customerId}/wishlist/${productId}`,{

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

    fetch(`http://127.0.0.1:8000/customers/${customerId}/recommendations`)

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

    <button onclick="buyNow(${product.id})">
        🛒 Buy Now
    </button>

</div>

`;

        });

    });

}