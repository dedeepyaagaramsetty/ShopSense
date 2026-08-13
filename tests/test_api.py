import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


# ============================================================
# BASIC API TEST
# ============================================================

def test_home():
    response = client.get("/")
    assert response.status_code == 200


# ============================================================
# VENDOR TESTS
# ============================================================

def test_get_vendors():
    response = client.get("/vendors/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_vendor():
    # Use an existing vendor ID from your database.
    response = client.get("/vendors/1")

    # Accept either success or not-found because the ID
    # may differ in the current database.
    assert response.status_code in [200, 404]


# ============================================================
# PRODUCT TESTS
# ============================================================

def test_get_products():
    response = client.get("/products/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_vendor_products():
    response = client.get("/products/vendor/1")

    assert response.status_code in [200, 404]


# ============================================================
# TRANSACTION TESTS
# ============================================================

def test_get_transactions():
    response = client.get("/transactions/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# ANALYTICS TESTS
# ============================================================

def test_revenue_analytics():
    response = client.get("/analytics/revenue")

    assert response.status_code == 200


def test_marketplace_analytics():
    response = client.get("/analytics/marketplace")

    assert response.status_code == 200


def test_vendor_performance():
    response = client.get("/analytics/vendor-performance")

    assert response.status_code == 200


def test_customer_insights():
    response = client.get("/analytics/customer-insights")

    assert response.status_code == 200


# ============================================================
# ML TEST
# ============================================================

def test_ml_forecast_summary():
    response = client.get("/ml/forecast-summary")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "products_trained" in data


# ============================================================
# MODEL REGISTRY TEST
# ============================================================

def test_model_registry():
    response = client.get("/analytics/model-registry")

    assert response.status_code == 200

    data = response.json()

    assert "model_name" in data
    assert "algorithm" in data
    assert "status" in data