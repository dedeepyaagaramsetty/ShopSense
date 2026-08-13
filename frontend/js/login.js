function adminLogin() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(email === "" || password === ""){

        document.getElementById("message").innerHTML =
        "Please enter email and password.";

        return;
    }

    fetch("http://localhost:8000/admin/login",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            email:email,
            password:password

        })

    })

    .then(response=>{

        if(!response.ok){

            throw new Error("Invalid Email or Password");

        }

        return response.json();

    })

    .then(data=>{

        localStorage.setItem("adminName",data.full_name);

        window.location.href="dashboard.html";

    })

    .catch(error=>{

        document.getElementById("message").innerHTML=error.message;

    });

}