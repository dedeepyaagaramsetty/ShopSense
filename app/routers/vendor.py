from app.models.order import Order
from app.models.order_item import OrderItem
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.database.database import get_db
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorResponse, VendorLogin

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

    total_products = db.query(Product).filter(
        Product.vendor_id == vendor_id
    ).count()

    total_inventory = db.query(
        func.sum(Product.stock)
    ).filter(
        Product.vendor_id == vendor_id
    ).scalar() or 0

    return {
    "vendor_id": vendor.id,
    "owner_name": vendor.owner_name,
    "business_name": vendor.business_name,
    "email": vendor.email,
    "phone": vendor.phone,
    "status": vendor.status,
    "total_products": total_products,
    "total_inventory": total_inventory
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

            total_revenue += item.price * item.quantity
            products_sold += item.quantity

            if order.id not in processed_orders:
                if order.status == "Completed":
                    completed_orders += 1
                elif order.status == "Pending":
                    pending_orders += 1

                processed_orders.add(order.id)

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