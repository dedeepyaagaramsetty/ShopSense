fetch("http://localhost:8000/analytics/model-registry")
    .then(response => response.json())
    .then(data => {

        console.log("ML Model Registry:", data);

        // =========================
        // Basic Model Information
        // =========================

        document.getElementById("modelName").innerText =
            data.model_name;

        document.getElementById("algorithm").innerText =
            data.algorithm;

        document.getElementById("status").innerText =
            data.status;

        document.getElementById("version").innerText =
            data.version;

        // =========================
        // ML Training Information
        // =========================

        document.getElementById("experiment").innerText =
            data.experiment;

        document.getElementById("productsTrained").innerText =
            data.products_trained;

        document.getElementById("averageMae").innerText =
            data.average_mae;

        document.getElementById("trainingDays").innerText =
            data.training_days + " Days";

        document.getElementById("forecastDays").innerText =
            data.forecast_days + " Days";

        document.getElementById("dataset").innerText =
            data.dataset;

        // =========================
        // Accuracy Chart
        // =========================

        new Chart(
            document.getElementById("accuracyChart"),
            {
                type: "doughnut",

                data: {
                    labels: [
                        "Accuracy",
                        "Remaining"
                    ],

                    datasets: [{
                        data: [
                            data.accuracy,
                            100 - data.accuracy
                        ]
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            }
        );

        // =========================
        // Pipeline Chart
        // =========================

        const pipelineCanvas = document.getElementById("pipelineChart");

if (pipelineCanvas) {

    new Chart(pipelineCanvas, {
        type: "bar",

        data: {
            labels: [
                "Data Collection",
                "Data Cleaning",
                "Model Training",
                "Model Evaluation",
                "Deployment"
            ],

            datasets: [{
                label: "Completion (%)",
                data: [100, 100, 100, 100, 100]
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,

                    ticks: {
                        callback: function(value) {
                            return value + "%";
                        }
                    }
                }
            },

            plugins: {
                legend: {
                    display: true
                },

                title: {
                    display: true,
                    text: "ShopSense Analytical Workflow"
                }
            }
        }
    });

}

        // =========================
        // Trained Products
        // =========================

        const list =
            document.getElementById("mlProductList");

        list.innerHTML = "";

        const products = [
            "Dell Inspiron",
            "Realme P4 Pro 5G Smartphone",
            "Men T-Shirt",
            "Sunflower Oil",
            "Samsung Galaxy S24",
            "Rice Bag 25kg",
            "iPhone 15"
        ];

        products.forEach(product => {

            const li =
                document.createElement("li");

            li.innerText = "✅ " + product;

            list.appendChild(li);

        });

    })

    .catch(error => {

        console.error(
            "Model Registry Error:",
            error
        );

    });