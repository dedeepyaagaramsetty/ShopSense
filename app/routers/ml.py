from fastapi import APIRouter
import mlflow
from mlflow.tracking import MlflowClient

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)

mlflow.set_tracking_uri("sqlite:///mlflow.db")


@router.get("/forecast-summary")
def forecast_summary():

    client = MlflowClient()

    experiment = client.get_experiment_by_name(
        "ShopSense Inventory Forecasting"
    )

    if experiment is None:
        return {
            "status": "Not Trained",
            "experiment": "ShopSense Inventory Forecasting",
            "model": "LinearRegression",
            "products_trained": 0,
            "average_mae": 0,
            "training_days": 30,
            "forecast_days": 7
        }

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"]
    )

    if not runs:
        return {
            "status": "No Runs",
            "experiment": "ShopSense Inventory Forecasting",
            "model": "LinearRegression",
            "products_trained": 0,
            "average_mae": 0,
            "training_days": 30,
            "forecast_days": 7
        }

    products = []
    maes = []

    for run in runs:

        product_name = run.data.params.get(
            "product_name"
        )

        mae = run.data.metrics.get("mae")

        if product_name:
            products.append(product_name)

        if mae is not None:
            maes.append(mae)

    average_mae = (
        round(sum(maes) / len(maes), 3)
        if maes
        else 0
    )

    latest_run = runs[0]

    return {
        "status": "Trained",
        "experiment": "ShopSense Inventory Forecasting",
        "model": "LinearRegression",
        "products_trained": len(products),
        "products": products,
        "average_mae": average_mae,
        "training_days": 30,
        "forecast_days": 7,
        "last_training": latest_run.info.start_time
    }