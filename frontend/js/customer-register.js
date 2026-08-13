function registerCustomer() {

    const full_name = document.getElementById("full_name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;
    const address = document.getElementById("address").value;

    if(
        full_name === "" ||
        email === "" ||
        phone === "" ||
        password === "" ||
        address === ""
    ){

        document.getElementById("message").innerHTML =
        "Please fill all fields.";

        return;

    }

    fetch("http://localhost:8000/customers/register",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            full_name,
            email,
            phone,
            password,
            address

        })

    })

    .then(async response=>{

        const data = await response.json();

        if(!response.ok){

            throw new Error(data.detail || "Registration Failed");

        }

        return data;

    })

    .then(data=>{

        alert("Registration Successful!");

        window.location.href="customer-login.html";

    })

    .catch(error=>{

        document.getElementById("message").innerHTML = error.message;

    });

}