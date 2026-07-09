fetch("http://127.0.0.1:8000/transactions/")
.then(response => response.json())
.then(data => {

    console.log(data);

    let table = document.getElementById("transactionTable");

    data.forEach(transaction => {

        let row = `
        <tr>
            <td>${transaction.order_id}</td>
            <td>${transaction.customer}</td>
            <td>${transaction.vendor}</td>
            <td>${transaction.product}</td>
            <td>${transaction.quantity}</td>
            <td>${transaction.amount}</td>
            <td>${transaction.status}</td>
        </tr>`;

        table.innerHTML += row;

    });

})
.catch(error => console.log(error));