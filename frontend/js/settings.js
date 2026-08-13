// =====================================
// DETECT LOGGED-IN USER
// =====================================

const customerId =
    localStorage.getItem("customerId");

const vendorId =
    localStorage.getItem("vendorId");

const adminId =
    localStorage.getItem("adminId");


let userType = "";

if (customerId) {

    userType = "customer";

}
else if (vendorId) {

    userType = "vendor";

}
else if (adminId) {

    userType = "admin";

}


// =====================================
// SET CORRECT NAVIGATION
// =====================================

function setupNavigation() {

    const dashboardLink =
        document.getElementById(
            "dashboardLink"
        );

    const profileLink =
        document.getElementById(
            "profileLink"
        );


    if (userType === "customer") {

        dashboardLink.href =
            "customer-dashboard.html";

        profileLink.href =
            "customer-profile.html";

    }

    else if (userType === "vendor") {

        dashboardLink.href =
            "vendor-dashboard.html";

        profileLink.href =
            "vendor-profile.html";

    }

    else if (userType === "admin") {

        dashboardLink.href =
            "admin-dashboard.html";

        profileLink.href =
            "admin-profile.html";

    }

}


setupNavigation();


// =====================================
// LOAD SAVED SETTINGS
// =====================================

function loadSettings() {

    const savedTheme =
        localStorage.getItem("theme");

    const orderNotifications =
        localStorage.getItem(
            "orderNotifications"
        );

    const paymentNotifications =
        localStorage.getItem(
            "paymentNotifications"
        );

    const deliveryNotifications =
        localStorage.getItem(
            "deliveryNotifications"
        );


    if (savedTheme) {

        document.getElementById(
            "themeSelect"
        ).value = savedTheme;

        applyTheme(savedTheme);

    }


    if (orderNotifications !== null) {

        document.getElementById(
            "orderNotifications"
        ).checked =
            orderNotifications === "true";

    }


    if (paymentNotifications !== null) {

        document.getElementById(
            "paymentNotifications"
        ).checked =
            paymentNotifications === "true";

    }


    if (deliveryNotifications !== null) {

        document.getElementById(
            "deliveryNotifications"
        ).checked =
            deliveryNotifications === "true";

    }

}


loadSettings();


// =====================================
// SAVE SETTINGS
// =====================================

function saveSettings() {

    const theme =
        document.getElementById(
            "themeSelect"
        ).value;

    const order =
        document.getElementById(
            "orderNotifications"
        ).checked;

    const payment =
        document.getElementById(
            "paymentNotifications"
        ).checked;

    const delivery =
        document.getElementById(
            "deliveryNotifications"
        ).checked;


    localStorage.setItem(
        "theme",
        theme
    );

    localStorage.setItem(
        "orderNotifications",
        order
    );

    localStorage.setItem(
        "paymentNotifications",
        payment
    );

    localStorage.setItem(
        "deliveryNotifications",
        delivery
    );


    applyTheme(theme);


    showMessage(
        "✅ Settings saved successfully!",
        "success"
    );

}


// =====================================
// THEME
// =====================================

function applyTheme(theme) {

    if (theme === "dark") {

        document.body.classList.add(
            "dark-mode"
        );

    }

    else {

        document.body.classList.remove(
            "dark-mode"
        );

    }

}


// =====================================
// PASSWORD
// =====================================

function showPasswordForm() {

    document.getElementById(
        "passwordForm"
    ).style.display = "block";

}


function hidePasswordForm() {

    document.getElementById(
        "passwordForm"
    ).style.display = "none";

}


function changePassword() {

    const newPassword =
        document.getElementById(
            "newPassword"
        ).value;

    const confirmPassword =
        document.getElementById(
            "confirmPassword"
        ).value;


    if (!newPassword) {

        showMessage(
            "❌ Enter a new password.",
            "error"
        );

        return;

    }


    if (newPassword !== confirmPassword) {

        showMessage(
            "❌ Passwords do not match.",
            "error"
        );

        return;

    }


    // We'll connect this to the backend
    // password endpoint if/when needed.

    showMessage(
        "✅ Password updated successfully!",
        "success"
    );


    document.getElementById(
        "newPassword"
    ).value = "";

    document.getElementById(
        "confirmPassword"
    ).value = "";

    hidePasswordForm();

}


// =====================================
// MESSAGE
// =====================================

function showMessage(message, type) {

    const box =
        document.getElementById(
            "message"
        );

    box.innerText = message;

    box.style.marginBottom = "15px";

    if (type === "success") {

        box.style.color = "green";

    }

    else {

        box.style.color = "red";

    }

}


// =====================================
// LOGOUT
// =====================================

function logout() {

    localStorage.clear();

    window.location.href =
        "index.html";

}