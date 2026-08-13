from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.vendor import Vendor
from app.models.product import Product
from app.database.database import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminLogin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/login")
def login(admin: AdminLogin, db: Session = Depends(get_db)):
    print("LOGIN EMAIL RECEIVED:", repr(admin.email))

    existing_admin = db.query(Admin).filter(
        Admin.email == admin.email
    ).first()
    print("ADMIN FOUND:", existing_admin)

    if not existing_admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    if existing_admin.password != admin.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    return {
        "message": "Admin Login Successful",
        "admin_id": existing_admin.id,
        "full_name": existing_admin.full_name
    }
@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total_vendors = db.query(Vendor).count()

    approved_vendors = db.query(Vendor).filter(
        Vendor.status == "Approved"
    ).count()

    pending_vendors = db.query(Vendor).filter(
        Vendor.status == "Pending"
    ).count()

    suspended_vendors = db.query(Vendor).filter(
        Vendor.status == "Suspended"
    ).count()

    total_products = db.query(Product).count()

    low_stock_products = db.query(Product).filter(
        Product.stock < 10
    ).count()

    return {
        "total_vendors": total_vendors,
        "approved_vendors": approved_vendors,
        "pending_vendors": pending_vendors,
        "suspended_vendors": suspended_vendors,
        "total_products": total_products,
        "low_stock_products": low_stock_products
    }
@router.get("/vendors")
def get_all_vendors(db: Session = Depends(get_db)):
    vendors = db.query(Vendor).all()
    return vendors


@router.put("/vendors/{vendor_id}/approve")
def approve_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    vendor.status = "Approved"
    db.commit()

    return {"message": "Vendor Approved Successfully"}


@router.put("/vendors/{vendor_id}/suspend")
def suspend_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    vendor.status = "Suspended"
    db.commit()

    return {"message": "Vendor Suspended Successfully"}
@router.get("/reports")
def marketplace_report(db: Session = Depends(get_db)):

    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.status == "Completed"
    ).scalar() or 0

    total_orders = db.query(Order).count()
    completed_orders = db.query(Order).filter(
         Order.status == "Completed"
    ).count()

    pending_orders = db.query(Order).filter(
        Order.status == "Pending"
    ).count()

    total_products = db.query(Product).count()

    total_vendors = db.query(Vendor).count()

    approved_vendors = db.query(Vendor).filter(
        Vendor.status == "Approved"
    ).count()

    pending_vendors = db.query(Vendor).filter(
        Vendor.status == "Pending"
    ).count()

    best_product = (
        db.query(
            Product.name,
            func.sum(OrderItem.quantity).label("sales")
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .first()
    )

    return {
    "total_revenue": total_revenue,
    "total_orders": total_orders,
    "completed_orders": completed_orders,
    "pending_orders": pending_orders,
    "total_products": total_products,
    "total_vendors": total_vendors,
    "approved_vendors": approved_vendors,
    "pending_vendors": pending_vendors,
    "best_selling_product": best_product.name if best_product else "No Data"
}
@router.get("/analytics")
def admin_analytics(db: Session = Depends(get_db)):

    total_customers = db.query(Customer).count()

    total_vendors = db.query(Vendor).count()

    total_products = db.query(Product).count()

    total_orders = db.query(Order).count()

    completed_orders = db.query(Order).filter(
        Order.status == "Completed"
    ).count()

    pending_orders = db.query(Order).filter(
        Order.status == "Pending"
    ).count()

    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.status == "Completed"
    ).scalar() or 0

    return {

    "total_customers": total_customers,

    "total_vendors": total_vendors,

    "total_products": total_products,

    "total_orders": total_orders,

    "completed_orders": completed_orders,

    "pending_orders": pending_orders,

    "total_revenue": total_revenue,

    "approved_vendors": db.query(Vendor).filter(
        Vendor.status == "Approved"
    ).count(),

    "pending_vendors": db.query(Vendor).filter(
        Vendor.status == "Pending"
    ).count(),

    "suspended_vendors": db.query(Vendor).filter(
        Vendor.status == "Suspended"
    ).count()

}