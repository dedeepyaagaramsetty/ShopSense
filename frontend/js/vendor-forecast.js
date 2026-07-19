const vendorId = localStorage.getItem("vendorId");

fetch(`http://127.0.0.1:8000/vendors/${vendorId}/forecast`)
.then(response => response.json())
.then(data => {

    // =========================
    // Summary Cards
    // =========================

    document.getElementById("totalProducts").innerText =
        data.total_products;

    document.getElementById("unitsSold").innerText =
        data.units_sold;

    document.getElementById("restockProducts").innerText =
        data.restock_products;

    document.getElementById("forecastAccuracy").innerText =
        data.forecast_accuracy;
    document.getElementById("forecastSummary").innerHTML =

`Total Products: <b>${data.total_products}</b><br>
Units Sold (30 Days): <b>${data.units_sold}</b><br>
Products Needing Restock: <b>${data.restock_products}</b><br>
Estimated Forecast Accuracy: <b>${data.forecast_accuracy}</b>`;

    // =========================
    // Forecast Table
    // =========================

    const table = document.getElementById("forecastTable");

    table.innerHTML = "";

    let productNames = [];
    let currentStock = [];
    let forecastStock = [];
    let unitsSold = [];
    console.log(data);
    console.log(data.forecast);

    data.forecast.forEach(product => {

        table.innerHTML += `
        <tr>
            <td>${product.product}</td>
            <td>${product.current_stock}</td>
            <td>${product.units_sold}</td>
            <td>${product.average_daily_sales}</td>
            <td>${product.forecast_next_week}</td>
            <td style="font-weight:bold;color:${
product.restock_needed ? "red" : "green"
}">
${product.restock_needed ? "Yes" : "No"}
</td>
        </tr>
        `;

        productNames.push(product.product);
        currentStock.push(product.current_stock);
        forecastStock.push(product.forecast_next_week);
        unitsSold.push(product.units_sold);

    });

    // =========================
    // Stock vs Forecast Chart
    // =========================

    new Chart(document.getElementById("stockChart"), {

        type: "bar",

        data: {

            labels: productNames,

            datasets: [

                {
                    label: "Current Stock",
                    data: currentStock
                },

                {
                    label: "Forecast (Next 7 Days)",
                    data: forecastStock
                }

            ]

        },

        options: {

            responsive: true,
            maintainAspectRatio:false,

            plugins: {

                title: {
                    display: true,
                    text: "Current Inventory vs Next 7-Day Demand"
                }

            }

        }

    });

    // =========================
    // Units Sold Chart
    // =========================

    new Chart(document.getElementById("salesChart"), {

        type: "bar",

        data: {

            labels: productNames,

            datasets: [

                {

                    label: "Units Sold (Last 30 Days)",

                    data: unitsSold

                }

            ]

        },

        options: {

            responsive: true,
            maintainAspectRatio:false,

            plugins: {

                title: {

                    display: true,

                    text: "Product Sales (Last 30 Days)"

                }

            }

        }

    });

});
function logout(){

    localStorage.clear();

    window.location.href = "index.html";

}