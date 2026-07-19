function customerLogin() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(email === "" || password === ""){

        document.getElementById("message").innerHTML =
        "Please enter email and password.";

        return;
    }

    fetch("http://127.0.0.1:8000/customers/login",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            email:email,
            password:password

        })

    })

    .then(async response=>{

        const data = await response.json();

        if(!response.ok){
            throw new Error(data.detail);
        }

        return data;

    })

    .then(data=>{

        localStorage.setItem("customerId", data.customer_id);
        localStorage.setItem("customerName", data.customer_name);

        window.location.href="customer-dashboard.html";

    })

    .catch(error=>{

        document.getElementById("message").innerHTML =
        error.message;

    });

}