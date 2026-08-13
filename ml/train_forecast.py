import sys
import os


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import mlflow
import mlflow.sklearn

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = "postgresql://postgres:06290727@localhost:5432/shopsense_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

db = SessionLocal()


# ============================================================
# MLflow CONFIGURATION
# ============================================================


mlflow.set_tracking_uri("sqlite:///mlflow.db")

mlflow.set_experiment("ShopSense Inventory Forecasting")


# ============================================================
# GET HISTORICAL SALES DATA
# ============================================================

def get_sales_data(product_id):

    today = datetime.utcnow()

    sales = []

    for days_ago in range(30, 0, -1):

        start_date = today - timedelta(days=days_ago)
        end_date = today - timedelta(days=days_ago - 1)

        items = (
            db.query(OrderItem)
            .join(Order)
            .filter(
                OrderItem.product_id == product_id,
                Order.order_date >= start_date,
                Order.order_date < end_date,
                Order.status == "Completed"
            )
            .all()
        )

        quantity = sum(
            item.quantity
            for item in items
        )

        sales.append(quantity)

    return sales


# ============================================================
# TRAIN FORECAST MODEL
# ============================================================

def train_model():

    products = db.query(Product).all()

    if not products:

        print("No products found in database.")

        return

    for product in products:

        sales = get_sales_data(product.id)

        # Need some historical data
        if sum(sales) == 0:

            print(
                f"Skipping {product.name} - "
                "no completed sales history."
            )

            continue

        X = [
            [i]
            for i in range(len(sales))
        ]

        y = sales

        model = LinearRegression()

        with mlflow.start_run(
            run_name=f"Forecast - {product.name}"
        ):

            # ------------------------------------------------
            # Train
            # ------------------------------------------------

            model.fit(X, y)

            predictions = model.predict(X)

            mae = mean_absolute_error(
                y,
                predictions
            )

            # ------------------------------------------------
            # Parameters
            # ------------------------------------------------

            mlflow.log_param(
                "product_id",
                product.id
            )

            mlflow.log_param(
                "product_name",
                product.name
            )

            mlflow.log_param(
                "training_days",
                30
            )

            mlflow.log_param(
                "model_type",
                "LinearRegression"
            )

            # ------------------------------------------------
            # Metrics
            # ------------------------------------------------

            mlflow.log_metric(
                "mae",
                float(mae)
            )

            mlflow.log_metric(
                "total_units_sold",
                float(sum(sales))
            )

            mlflow.log_metric(
                "average_daily_sales",
                float(sum(sales) / 30)
            )

            # ------------------------------------------------
            # Save Model
            # ------------------------------------------------

            mlflow.sklearn.log_model(
                model,
                "forecast_model"
            )

            print(
                f"Trained model for {product.name}"
            )

            print(
                f"MAE: {mae:.2f}"
            )

    print("\nMLflow training completed.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    try:

        train_model()

    finally:

        db.close()