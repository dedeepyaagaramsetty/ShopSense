const vendorId = localStorage.getItem("vendorId");

fetch(`http://127.0.0.1:8000/transactions/vendor/${vendorId}`)
.then(response => response.json())
.then(data => {

    let table = document.getElementById("transactionTable");

    table.innerHTML = "";

    if (data.length === 0) {

        table.innerHTML = `
        <tr>
            <td colspan="6" style="text-align:center;">
                No transactions available.
            </td>
        </tr>
        `;

        return;
    }

    data.forEach(transaction => {

        table.innerHTML += `
        <tr>
            <td>${transaction.order_id}</td>
            <td>${transaction.customer}</td>
            <td>${transaction.product}</td>
            <td>${transaction.quantity}</td>
            <td>₹${transaction.amount}</td>
            <td>${transaction.status}</td>
        </tr>
        `;

    });

});