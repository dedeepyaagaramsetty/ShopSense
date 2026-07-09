function customerLogin() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(email === "" || password === ""){

        document.getElementById("message").innerHTML =
        "Please enter email and password.";

        return;
    }

    window.location.href = "customer-dashboard.html";

}