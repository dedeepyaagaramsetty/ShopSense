fetch("http://localhost:8000/admin/vendors")
.then(response => response.json())
.then(vendors => {

    let table = document.getElementById("vendorTable");

    vendors.forEach(vendor => {

        let approveButton = "";
        let suspendButton = "";

        if (vendor.status === "Pending") {
            approveButton = `<button onclick="approveVendor(${vendor.id})">Approve</button>`;
            suspendButton = `<button onclick="suspendVendor(${vendor.id})">Suspend</button>`;
        }
        else if (vendor.status === "Approved") {
            approveButton = `<button disabled>Approved</button>`;
            suspendButton = `<button onclick="suspendVendor(${vendor.id})">Suspend</button>`;
        }
        else if (vendor.status === "Suspended") {
            approveButton = `<button onclick="approveVendor(${vendor.id})">Approve</button>`;
            suspendButton = `<button disabled>Suspended</button>`;
        }

        table.innerHTML += `
        <tr>
            <td>${vendor.id}</td>
            <td>${vendor.owner_name}</td>
            <td>${vendor.business_name}</td>
            <td>${vendor.email}</td>
            <td>${vendor.phone}</td>
            <td>${vendor.status}</td>
            <td>${approveButton}</td>
            <td>${suspendButton}</td>
        </tr>
        `;

    });

});

function approveVendor(id) {

    fetch(`http://localhost:8000/admin/vendors/${id}/approve`, {
        method: "PUT"
    })
    .then(() => {
        alert("Vendor Approved");
        location.reload();
    });

}

function suspendVendor(id) {

    fetch(`http://localhost:8000/admin/vendors/${id}/suspend`, {
        method: "PUT"
    })
    .then(() => {
        alert("Vendor Suspended");
        location.reload();
    });

}
function searchVendor(){

    let input = document.getElementById("searchVendor").value.toLowerCase();

    let rows = document.querySelectorAll("#vendorTable tr");

    rows.forEach(row => {

        let text = row.innerText.toLowerCase();

        if(text.includes(input)){
            row.style.display="";
        }
        else{
            row.style.display="none";
        }

    });

}