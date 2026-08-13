fetch("http://localhost:8000/analytics/vendor-performance")

.then(response => response.json())

.then(data => {

    // Top Vendor Cards

    document.getElementById("topVendor").innerText =
        data[0].business_name;

    document.getElementById("highestRevenue").innerText =
        data[0].revenue;

    document.getElementById("topOrders").innerText =
        data[0].completed_orders;

    document.getElementById("topAverage").innerText =
        data[0].average_order_value;

    // Leaderboard

    const table = document.getElementById("leaderboard");

    table.innerHTML = "";

    let vendorNames = [];
    let revenues = [];

    data.forEach(vendor => {

        

        let medal = "";

        if(vendor.rank === 1)
            medal = "🥇";
        else if(vendor.rank === 2)
            medal = "🥈";
        else if(vendor.rank === 3)
            medal = "🥉";

        table.innerHTML += `

        <tr>

            <td>${medal} ${vendor.rank}</td>

            <td>${vendor.business_name}</td>

            <td>₹${vendor.revenue}</td>

            <td>${vendor.completed_orders}</td>

            <td>₹${vendor.average_order_value}</td>

        </tr>

`;

        vendorNames.push(vendor.business_name);

        revenues.push(vendor.revenue);

    });

    // Revenue Chart

    new Chart(document.getElementById("benchmarkChart"), {

        type: "bar",

        data: {

            labels: vendorNames,

            datasets: [

{

label: "Revenue (₹)",

data: revenues,

borderWidth: 1

}

]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            indexAxis: 'y',
            plugins:{

            legend:{
                display:true
            },

            title:{
                display:true,
                text:"Vendor Revenue Ranking"
            }

            }

        }

    });

});