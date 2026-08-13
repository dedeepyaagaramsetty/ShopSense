function vendorLogin() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(email === "" || password === ""){

        document.getElementById("message").innerHTML =
        "Please enter email and password.";

        return;
    }

    fetch("http://localhost:8000/vendors/login",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            email:email,
            password:password

        })

    })

    .then(async response => {

        const data = await response.json();

        if(!response.ok){
            throw new Error(data.detail);
    }

        return data;

})

    .then(data=>{
        localStorage.setItem("vendorId", data.vendor_id);

        localStorage.setItem("vendorName",data.business_name);

        window.location.href="vendor-dashboard.html";

    })

    .catch(error=>{

        document.getElementById("message").innerHTML=error.message;

    });

}