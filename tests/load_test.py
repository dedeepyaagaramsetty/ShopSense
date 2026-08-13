from locust import HttpUser, task, between


class ShopSenseUser(HttpUser):

    wait_time = between(1, 3)

    @task(3)
    def get_vendors(self):
        self.client.get("/vendors/")

    @task(3)
    def get_products(self):
        self.client.get("/products/")

    @task(2)
    def get_revenue(self):
        self.client.get("/analytics/revenue")

    @task(2)
    def get_marketplace(self):
        self.client.get("/analytics/marketplace")

    @task(2)
    def get_vendor_performance(self):
        self.client.get("/analytics/vendor-performance")

    @task(1)
    def get_ml_summary(self):
        self.client.get("/ml/forecast-summary")

    @task(1)
    def get_model_registry(self):
        self.client.get("/analytics/model-registry")