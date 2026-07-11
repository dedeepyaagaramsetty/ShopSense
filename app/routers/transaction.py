from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer
from app.models.product import Product
from app.models.vendor import Vendor

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_transactions(db: Session = Depends(get_db)):

    data = []

    orders = db.query(Order).all()

    for order in orders:

        customer = db.query(Customer).filter(
            Customer.id == order.customer_id
        ).first()

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            vendor = db.query(Vendor).filter(
                Vendor.id == product.vendor_id
            ).first()

            data.append({
                "order_id": order.id,
                "customer": customer.full_name,
                "vendor": vendor.owner_name,
                "product": product.name,
                "quantity": item.quantity,
                "amount": item.price * item.quantity,
                "status": order.status
            })

    return data
@router.get("/vendor/{vendor_id}")
def get_vendor_transactions(vendor_id: int, db: Session = Depends(get_db)):

    data = []

    orders = db.query(Order).all()

    for order in orders:

        customer = db.query(Customer).filter(
            Customer.id == order.customer_id
        ).first()

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            if product.vendor_id != vendor_id:
                continue

            vendor = db.query(Vendor).filter(
                Vendor.id == vendor_id
            ).first()

            data.append({
                "order_id": order.id,
                "customer": customer.full_name,
                "product": product.name,
                "quantity": item.quantity,
                "amount": item.price * item.quantity,
                "status": order.status
            })

    return data