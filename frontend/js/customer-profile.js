const customerId = localStorage.getItem("customerId");


// ================================
// LOAD CUSTOMER PROFILE
// ================================

function loadProfile() {

    fetch(`http://localhost:8000/customers/${customerId}/profile`)

        .then(async response => {

            if (!response.ok) {

                const data = await response.json();

                throw new Error(
                    data.detail || "Failed to load profile"
                );

            }

            return response.json();

        })

        .then(customer => {

            // View mode

            document.getElementById("name").innerText =
                customer.full_name || "";

            document.getElementById("email").innerText =
                customer.email || "";

            document.getElementById("phone").innerText =
                customer.phone || "";

            document.getElementById("address").innerText =
                customer.address || "Not provided";


            if (customer.created_at) {

                document.getElementById("joined").innerText =
                    new Date(
                        customer.created_at
                    ).toLocaleDateString();

            }


            // Fill edit fields

            document.getElementById("editName").value =
                customer.full_name || "";

            document.getElementById("editEmail").value =
                customer.email || "";

            document.getElementById("editPhone").value =
                customer.phone || "";

            document.getElementById("editAddress").value =
                customer.address || "";

        })

        .catch(error => {

            console.error("Profile error:", error);

            showMessage(
                "❌ " + error.message,
                "error"
            );

        });

}


// Load profile when page opens
loadProfile();


// ================================
// ENABLE EDIT MODE
// ================================

function enableEdit() {

    document.getElementById("profileView").style.display =
        "none";

    document.getElementById("profileEdit").style.display =
        "block";

    clearMessage();

}


// ================================
// CANCEL EDIT
// ================================

function cancelEdit() {

    document.getElementById("profileEdit").style.display =
        "none";

    document.getElementById("profileView").style.display =
        "block";

    clearMessage();

    // Reload original values
    loadProfile();

}


// ================================
// SAVE PROFILE
// ================================

function saveProfile() {

    const fullName =
        document.getElementById("editName").value.trim();

    const email =
        document.getElementById("editEmail").value.trim();

    const phone =
        document.getElementById("editPhone").value.trim();

    const address =
        document.getElementById("editAddress").value.trim();


    // Basic validation

    if (!fullName) {

        showMessage(
            "❌ Full name is required.",
            "error"
        );

        return;

    }


    if (!email) {

        showMessage(
            "❌ Email is required.",
            "error"
        );

        return;

    }


    if (!phone) {

        showMessage(
            "❌ Phone number is required.",
            "error"
        );

        return;

    }


    // ================================
    // UPDATE REQUEST
    // ================================

    fetch(
        `http://localhost:8000/customers/${customerId}/profile`,
        {

            method: "PUT",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body: JSON.stringify({

                full_name: fullName,

                email: email,

                phone: phone,

                address: address

            })

        }
    )

    .then(async response => {

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to update profile"
            );

        }

        return data;

    })

    .then(data => {

        showMessage(
            "✅ Profile updated successfully!",
            "success"
        );


        // Return to view mode

        document.getElementById(
            "profileEdit"
        ).style.display = "none";


        document.getElementById(
            "profileView"
        ).style.display = "block";


        // Reload profile

        loadProfile();

    })

    .catch(error => {

        console.error(
            "Update profile error:",
            error
        );

        showMessage(
            "❌ " + error.message,
            "error"
        );

    });

}


// ================================
// MESSAGE
// ================================

function showMessage(message, type) {

    const messageBox =
        document.getElementById("message");

    messageBox.innerText = message;

    if (type === "success") {

        messageBox.style.color = "green";

    }
    else {

        messageBox.style.color = "red";

    }

}


function clearMessage() {

    document.getElementById(
        "message"
    ).innerText = "";

}


// ================================
// LOGOUT
// ================================

function logout() {

    localStorage.clear();

    window.location.href =
        "index.html";

}