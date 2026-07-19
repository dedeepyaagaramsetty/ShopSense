const customerId = localStorage.getItem("customerId");

fetch(`http://127.0.0.1:8000/customers/${customerId}/profile`)
.then(response => response.json())
.then(customer => {

    document.getElementById("name").innerText =
        customer.full_name;

    document.getElementById("email").innerText =
        customer.email;

    document.getElementById("phone").innerText =
        customer.phone;

    document.getElementById("address").innerText =
        customer.address;

    document.getElementById("joined").innerText =
        new Date(customer.created_at).toLocaleDateString();

});

function logout(){

    localStorage.clear();

    window.location.href="index.html";

}