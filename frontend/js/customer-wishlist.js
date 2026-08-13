const customerId = localStorage.getItem("customerId");

fetch(`http://localhost:8000/customers/${customerId}/wishlist`)
.then(response => response.json())
.then(products => {

    const container = document.getElementById("wishlistContainer");

    container.innerHTML = "";

    if(products.length === 0){

        container.innerHTML = "<h3 style='text-align:center;'>❤️ Your wishlist is empty.</h3>";

        return;
    }

    products.forEach(product => {

        let icon = "📦";

        if(product.category_id === 1){
            icon = "💻";   // Electronics
        }
        else if(product.category_id === 2){
            icon = "📱";   // Mobiles
        }
        else if(product.category_id === 3){
            icon = "💻";   // Laptops
        }
        else if(product.category_id === 4){
            icon = "👕";   // Fashion
        }
        else if(product.category_id === 5){
            icon = "🛒";   // Grocery
        }

        container.innerHTML += `

        <div class="product-card">

            <div class="product-icon">
                ${icon}
            </div>

            <h3>${product.name}</h3>

            <p>${product.description}</p>

            <h2>₹${product.price}</h2>

            <p>Stock: ${product.stock}</p>

            <button onclick="window.location.href='customer-dashboard.html'">
                🛍️ Buy Now
            </button>

        </div>

        `;

    });

});

function logout(){

    localStorage.clear();

    window.location.href = "index.html";

}