const vendorId = localStorage.getItem("vendorId");


// =====================================
// LOAD VENDOR PROFILE
// =====================================

function loadProfile() {

    if (!vendorId) {

        showMessage(
            "❌ Vendor session not found. Please login again.",
            "error"
        );

        return;
    }


    fetch(
        `http://localhost:8000/vendors/${vendorId}`
    )

    .then(async response => {

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Failed to load profile"
            );

        }

        return data;

    })

    .then(vendor => {

        // VIEW MODE

        document.getElementById("ownerName").innerText =
            vendor.owner_name || "";

        document.getElementById("businessName").innerText =
            vendor.business_name || "";

        document.getElementById("email").innerText =
            vendor.email || "";

        document.getElementById("phone").innerText =
            vendor.phone || "";

        document.getElementById("status").innerText =
            vendor.status || "";


        // EDIT MODE

        document.getElementById("editOwnerName").value =
            vendor.owner_name || "";

        document.getElementById("editBusinessName").value =
            vendor.business_name || "";

        document.getElementById("editEmail").value =
            vendor.email || "";

        document.getElementById("editPhone").value =
            vendor.phone || "";

        document.getElementById("editStatus").innerText =
            vendor.status || "";

    })

    .catch(error => {

        console.error(
            "Vendor profile error:",
            error
        );

        showMessage(
            "❌ " + error.message,
            "error"
        );

    });

}


loadProfile();


// =====================================
// ENABLE EDIT
// =====================================

function enableEdit() {

    document.getElementById(
        "profileView"
    ).style.display = "none";

    document.getElementById(
        "profileEdit"
    ).style.display = "block";

    clearMessage();

}


// =====================================
// CANCEL EDIT
// =====================================

function cancelEdit() {

    document.getElementById(
        "profileEdit"
    ).style.display = "none";

    document.getElementById(
        "profileView"
    ).style.display = "block";

    clearMessage();

    loadProfile();

}


// =====================================
// SAVE PROFILE
// =====================================

function saveProfile() {

    const ownerName =
        document.getElementById(
            "editOwnerName"
        ).value.trim();

    const businessName =
        document.getElementById(
            "editBusinessName"
        ).value.trim();

    const email =
        document.getElementById(
            "editEmail"
        ).value.trim();

    const phone =
        document.getElementById(
            "editPhone"
        ).value.trim();


    if (!ownerName) {

        showMessage(
            "❌ Owner name is required.",
            "error"
        );

        return;
    }


    if (!businessName) {

        showMessage(
            "❌ Business name is required.",
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


    fetch(
        `http://localhost:8000/vendors/${vendorId}/profile`,
        {

            method: "PUT",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body: JSON.stringify({

                owner_name: ownerName,

                business_name: businessName,

                email: email,

                phone: phone

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


        document.getElementById(
            "profileEdit"
        ).style.display = "none";

        document.getElementById(
            "profileView"
        ).style.display = "block";


        loadProfile();

    })

    .catch(error => {

        console.error(
            "Update vendor profile error:",
            error
        );

        showMessage(
            "❌ " + error.message,
            "error"
        );

    });

}


// =====================================
// MESSAGES
// =====================================

function showMessage(message, type) {

    const box =
        document.getElementById("message");

    box.innerText = message;

    box.style.marginBottom = "15px";

    if (type === "success") {

        box.style.color = "green";

    } else {

        box.style.color = "red";

    }

}


function clearMessage() {

    document.getElementById(
        "message"
    ).innerText = "";

}


// =====================================
// LOGOUT
// =====================================

function logout() {

    localStorage.clear();

    window.location.href =
        "index.html";

}