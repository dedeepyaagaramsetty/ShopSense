function registerVendor() {

    const owner_name = document.getElementById("owner_name").value;
    const business_name = document.getElementById("business_name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;

    if (
        owner_name === "" ||
        business_name === "" ||
        email === "" ||
        phone === "" ||
        password === ""
    ) {

        document.getElementById("message").innerHTML =
        "Please fill all fields.";

        return;
    }

    fetch("http://127.0.0.1:8000/vendors/register", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            owner_name,
            business_name,
            email,
            phone,
            password

        })

    })

    .then(response => {

        if (!response.ok) {
            throw new Error("Registration Failed");
        }

        return response.json();

    })

    .then(data => {

        alert("Registration Successful! Wait for Admin Approval.");

        window.location.href = "vendor-login.html";

    })

    .catch(error => {

        document.getElementById("message").innerHTML = error.message;

    });

}