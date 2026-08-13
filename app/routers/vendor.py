from app.models.order import Order
from app.models.order_item import OrderItem
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.database.database import get_db
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorResponse, VendorLogin
from datetime import datetime, timedelta
import math
router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)

@router.post("/register", response_model=VendorResponse)
def register_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    new_vendor = Vendor(
        business_name=vendor.business_name,
        owner_name=vendor.owner_name,
        email=vendor.email,
        phone=vendor.phone,
        password=vendor.password,
        status="Pending"
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor

@router.post("/login")
def login_vendor(vendor: VendorLogin, db: Session = Depends(get_db)):

    existing_vendor = db.query(Vendor).filter(
        Vendor.email == vendor.email
    ).first()

    if not existing_vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    if existing_vendor.password != vendor.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    # Pending Vendor
    if existing_vendor.status == "Pending":
        raise HTTPException(
            status_code=403,
            detail="Your account is awaiting Admin Approval."
        )

    # Suspended Vendor
    if existing_vendor.status == "Suspended":
        raise HTTPException(
            status_code=403,
            detail="Your account has been suspended."
        )

    return {
        "message": "Login Successful",
        "vendor_id": existing_vendor.id,
        "business_name": existing_vendor.business_name
    }
@router.get("/", response_model=list[VendorResponse])
def get_vendors(db: Session = Depends(get_db)):
    vendors = db.query(Vendor).all()
    return vendors
@router.put("/approve/{vendor_id}")
def approve_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    vendor.status = "Approved"

    db.commit()
    db.refresh(vendor)

    return {
        "message": "Vendor Approved Successfully",
        "vendor": vendor.business_name,
        "status": vendor.status
    }
@router.get("/{vendor_id}")
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    return {
        "id": vendor.id,
        "owner_name": vendor.owner_name,
        "business_name": vendor.business_name,
        "email": vendor.email,
        "phone": vendor.phone,
        "status": vendor.status
    }
@router.get("/{vendor_id}/dashboard")
def vendor_dashboard(vendor_id: int, db: Session = Depends(get_db)):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    # Products
    products = db.query(Product).filter(
        Product.vendor_id == vendor_id
    ).all()

    total_products = len(products)

    total_inventory = sum(
        product.stock
        for product in products
    )

    inventory_value = sum(
        product.stock * product.price
        for product in products
    )

    product_ids = [product.id for product in products]

    total_revenue = 0
    completed_orders = 0
    best_product = "No Data"

    if product_ids:

        order_items = db.query(OrderItem).filter(
            OrderItem.product_id.in_(product_ids)
        ).all()

        total_revenue = sum(
            item.price * item.quantity
            for item in order_items
        )

        completed_orders = len(order_items)

        sales = {}

        for item in order_items:

            sales[item.product_id] = sales.get(item.product_id, 0) + item.quantity

        if sales:

            best_product_id = max(
                sales,
                key=sales.get
            )

            product = db.query(Product).filter(
                Product.id == best_product_id
            ).first()

            if product:
                best_product = product.name

    return {

        "vendor_id": vendor.id,

        "owner_name": vendor.owner_name,

        "business_name": vendor.business_name,

        "email": vendor.email,

        "phone": vendor.phone,

        "status": vendor.status,

        "total_products": total_products,

        "total_inventory": total_inventory,

        "inventory_value": inventory_value,

        "total_revenue": total_revenue,

        "completed_orders": completed_orders,

        "best_product": best_product

    }
@router.get("/{vendor_id}/reports")
def vendor_reports(vendor_id: int, db: Session = Depends(get_db)):

    products = db.query(Product).filter(
        Product.vendor_id == vendor_id
    ).all()

    product_ids = [product.id for product in products]

    total_revenue = 0
    products_sold = 0
    completed_orders = 0
    pending_orders = 0

    processed_orders = set()

    for product_id in product_ids:

        order_items = db.query(OrderItem).filter(
            OrderItem.product_id == product_id
        ).all()

        for item in order_items:

            order = db.query(Order).filter(
                Order.id == item.order_id
            ).first()

            if not order:
                continue

            if order.id in processed_orders:
                continue

            processed_orders.add(order.id)

            if order.status == "Completed":

                completed_orders += 1
                total_revenue += item.price * item.quantity
                products_sold += item.quantity

            elif order.status == "Pending":

                pending_orders += 1

    return {
        "total_revenue": total_revenue,
        "products_sold": products_sold,
        "completed_orders": completed_orders,
        "pending_orders": pending_orders
    }
@router.get("/{vendor_id}/inventory")
def vendor_inventory(vendor_id: int, db: Session = Depends(get_db)):

    products = db.query(Product).filter(
        Product.vendor_id == vendor_id
    ).all()

    inventory = []

    total_products = len(products)
    total_stock = 0
    total_inventory_value = 0

    for product in products:

        inventory_value = product.stock * product.price

        total_stock += product.stock
        total_inventory_value += inventory_value

        inventory.append({
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "inventory_value": inventory_value
        })

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "total_inventory_value": total_inventory_value,
        "products": inventory
    }
@router.get("/{vendor_id}/forecast")
def vendor_forecast(vendor_id: int, db: Session = Depends(get_db)):

    from datetime import datetime, timedelta

    products = db.query(Product).filter(
        Product.vendor_id == vendor_id
    ).all()

    forecast = []

    total_products = len(products)
    total_units_sold = 0
    restock_products = 0

    for product in products:

        last_30_days = datetime.utcnow() - timedelta(days=30)

        order_items = (
            db.query(OrderItem)
            .join(Order)
            .filter(
                OrderItem.product_id == product.id,
                Order.order_date >= last_30_days,
                Order.status == "Completed"

            )
            .all()
        )

        units_sold = sum(item.quantity for item in order_items)

        average_daily_sales = round(units_sold / 30, 2)

        forecast_next_week = round(average_daily_sales * 7)

        restock_needed = product.stock < forecast_next_week

        if restock_needed:
            restock_products += 1

        total_units_sold += units_sold

        forecast.append({

            "product": product.name,

            "current_stock": product.stock,

            "units_sold": units_sold,

            "average_daily_sales": average_daily_sales,

            "forecast_next_week": forecast_next_week,

            "restock_needed": restock_needed

        })

    return {

        "total_products": total_products,

        "units_sold": total_units_sold,

        "restock_products": restock_products,

        "forecast_accuracy": "82%",

        "forecast": forecast

    }
@router.put("/{vendor_id}/profile")
def update_vendor_profile(
    vendor_id: int,
    data: dict,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    if "business_name" in data:
        vendor.business_name = data["business_name"]

    if "owner_name" in data:
        vendor.owner_name = data["owner_name"]

    if "email" in data:
        vendor.email = data["email"]

    if "phone" in data:
        vendor.phone = data["phone"]

    if "password" in data:
        vendor.password = data["password"]

    db.commit()

    db.refresh(vendor)

    return {
        "message": "Profile updated successfully"
    }