from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database.database import get_db
from app.models.vendor import Vendor
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/vendor-performance")
def vendor_performance(db: Session = Depends(get_db)):

    vendors = db.query(Vendor).all()

    result = []

    for vendor in vendors:

        products = db.query(Product).filter(
            Product.vendor_id == vendor.id
        ).all()

        product_ids = [p.id for p in products]

        revenue = 0
        completed_orders = set()

        if product_ids:

            order_items = db.query(OrderItem).filter(
                OrderItem.product_id.in_(product_ids)
            ).all()

            for item in order_items:

                order = db.query(Order).filter(
                    Order.id == item.order_id,
                    Order.status == "Completed"
                ).first()

                if order:

                    revenue += item.price * item.quantity
                    completed_orders.add(order.id)

        total_orders = len(completed_orders)

        average_order_value = (
            round(revenue / total_orders, 2)
            if total_orders > 0 else 0
        )

        result.append({

            "vendor_id": vendor.id,
            "business_name": vendor.business_name,
            "revenue": revenue,
            "completed_orders": total_orders,
            "average_order_value": average_order_value

        })

    result.sort(key=lambda x: x["revenue"], reverse=True)

    for index, vendor in enumerate(result):
        vendor["rank"] = index + 1

    return result


@router.get("/customer-insights")
def customer_insights(db: Session = Depends(get_db)):

    total_customers = db.query(Customer).count()

    total_orders = db.query(Order).count()

    completed_orders = db.query(Order).filter(
        Order.status == "Completed"
    ).count()

    pending_orders = db.query(Order).filter(
        Order.status == "Pending"
    ).count()

    return {

        "total_customers": total_customers,
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "pending_orders": pending_orders

    }


@router.get("/revenue")
def revenue(db: Session = Depends(get_db)):

    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.status == "Completed"
    ).scalar() or 0

    return {

        "total_revenue": total_revenue

    }


@router.get("/marketplace")
def marketplace(db: Session = Depends(get_db)):

    return {

        "vendors": db.query(Vendor).count(),
        "customers": db.query(Customer).count(),
        "products": db.query(Product).count(),
        "orders": db.query(Order).count()

    }
@router.get("/revenue-analysis")
def revenue_analysis(db: Session = Depends(get_db)):

    now = datetime.utcnow()

    current_month = now.month
    current_year = now.year

    if current_month == 1:
        last_month = 12
        last_year = current_year - 1
    else:
        last_month = current_month - 1
        last_year = current_year

    completed_orders = db.query(Order).filter(
        Order.status == "Completed"
    ).all()

    gmv = sum(order.total_amount for order in completed_orders)

    completed_count = len(completed_orders)

    average_order_value = (
        gmv / completed_count
        if completed_count > 0 else 0
    )

    estimated_profit = gmv * 0.20

    current_month_revenue = sum(
        order.total_amount
        for order in completed_orders
        if order.order_date.month == current_month
        and order.order_date.year == current_year
    )

    last_month_revenue = sum(
        order.total_amount
        for order in completed_orders
        if order.order_date.month == last_month
        and order.order_date.year == last_year
    )

    if last_month_revenue == 0:
        growth_percentage = 0
    else:
        growth_percentage = round(
            ((current_month_revenue - last_month_revenue)
            / last_month_revenue) * 100,
            2
        )

    return {

        "gmv": gmv,

        "completed_orders": completed_count,

        "average_order_value": round(average_order_value, 2),

        "estimated_profit": round(estimated_profit, 2),

        "current_month_revenue": current_month_revenue,

        "last_month_revenue": last_month_revenue,

        "growth_percentage": growth_percentage

    }
@router.get("/model-registry")
def model_registry():

    return {
        "model_name": "Inventory Forecast v1",
        "algorithm": "Linear Regression",
        "experiment": "ShopSense Inventory Forecasting",

        "products_trained": 7,
        "average_mae": 0.193,

        "training_days": 30,
        "forecast_days": 7,

        "accuracy": 82,
        "version": "v1.0",
        "status": "Production",

        "dataset": "ShopSense Transactions Dataset",

        "pipeline": {
            "data_collection": 100,
            "data_cleaning": 100,
            "model_training": 100,
            "evaluation": 100,
            "deployment": 100
        }
    }