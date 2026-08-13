from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.wishlist import Wishlist
from app.models.product import Product
from app.database.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerLogin
from app.models.order import Order
from app.models.customer import Customer
from sqlalchemy import func
from app.models.notification import Notification
from app.schemas.customer import (
    CustomerCreate,
    CustomerLogin,
    CustomerResponse
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)
@router.post("/register", response_model=CustomerResponse)
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    new_customer = Customer(

        full_name=customer.full_name,

        email=customer.email,

        phone=customer.phone,

        password=customer.password,

        address=customer.address

    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    return new_customer

# ----------------------------
# Customer Login
# ----------------------------
@router.post("/login")
def customer_login(customer: CustomerLogin,
                   db: Session = Depends(get_db)):

    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if not existing_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if existing_customer.password != customer.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
        "message": "Login Successful",
        "customer_id": existing_customer.id,
        "customer_name": existing_customer.full_name
    }


# ----------------------------
# Customer Dashboard
# ----------------------------
@router.get("/{customer_id}")
def get_customer(customer_id: int,
                 db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "id": customer.id,
        "full_name": customer.full_name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address
    }
@router.get("/{customer_id}/dashboard")
def customer_dashboard(customer_id: int, db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Total Orders
    total_orders = db.query(Order).filter(
        Order.customer_id == customer_id
    ).count()

    # Completed Orders
    completed_orders = db.query(Order).filter(
        Order.customer_id == customer_id,
        Order.status == "Completed"
    ).count()

    # Pending Orders
    pending_orders = db.query(Order).filter(
        Order.customer_id == customer_id,
        Order.status == "Pending"
    ).count()

    # Total Amount Spent
    total_spent = db.query(
        func.sum(Order.total_amount)
    ).filter(
        Order.customer_id == customer_id,
        Order.status == "Completed"
    ).scalar() or 0

    # Average Order Value
    average_spent = round(
        total_spent / completed_orders, 2
    ) if completed_orders else 0

    return {
        "full_name": customer.full_name,
        "email": customer.email,
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "pending_orders": pending_orders,
        "total_spent": total_spent,
        "average_spent": average_spent
    }
@router.post("/{customer_id}/buy/{product_id}")
def buy_product(
    customer_id: int,
    product_id: int,
    order_data: dict,
    db: Session = Depends(get_db)
):

    # -----------------------------
    # Check customer
    # -----------------------------

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # -----------------------------
    # Check product
    # -----------------------------

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # -----------------------------
    # Check stock
    # -----------------------------

    quantity = order_data.get("quantity", 1)

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid quantity"
        )

    if product.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} items available"
        )

    # -----------------------------
    # Get order information
    # -----------------------------

    address = order_data.get(
        "address",
        customer.address
    )

    payment_method = order_data.get(
        "payment_method"
    )

    if not payment_method:
        raise HTTPException(
            status_code=400,
            detail="Payment method is required"
        )

    # -----------------------------
    # Calculate total
    # -----------------------------

    total_amount = product.price * quantity

    # -----------------------------
    # Create Order
    # -----------------------------

    order = Order(

        customer_id=customer_id,

        total_amount=total_amount,

        status="Completed",

        payment_method=payment_method,

        payment_status="Paid",

        delivery_status="Processing",

        address=address,

        order_date=datetime.utcnow()

    )

    db.add(order)

    db.commit()

    db.refresh(order)

    # -----------------------------
    # Create Order Item
    # -----------------------------

    order_item = OrderItem(

        order_id=order.id,

        product_id=product.id,

        quantity=quantity,

        price=product.price

    )

    db.add(order_item)

    # -----------------------------
    # Reduce stock
    # -----------------------------

    product.stock -= quantity

    db.commit()

    return {

        "message": "Payment successful! Order placed successfully.",

        "order_id": order.id,

        "product": product.name,

        "quantity": quantity,

        "amount": total_amount,

        "payment_method": payment_method,

        "payment_status": "Paid",

        "delivery_status": "Processing"

    }
@router.post("/{customer_id}/orders/{order_id}/pay")
def pay_for_order(
    customer_id: int,
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.customer_id == customer_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.payment_status == "Paid":
        return {
            "message": "Payment already completed"
        }

    order.payment_status = "Paid"
    order.status = "Completed"
    item = db.query(OrderItem).filter(
    OrderItem.order_id == order.id
).first()

    product = None

    if item:
        product = db.query(Product).filter(
        Product.id == item.product_id
    ).first()

    customer_notification = Notification(
    user_type="customer",
    user_id=customer_id,
    message=f"Payment completed successfully for Order #{order.id}."
    )

    db.add(customer_notification)

    if product:

        vendor_notification = Notification(
        user_type="vendor",
        user_id=product.vendor_id,
        message=f"Payment completed for Order #{order.id}."
    )

    db.add(vendor_notification)

    db.commit()

    return {
        "message": "UPI Payment Successful",
        "order_id": order.id,
        "payment_status": order.payment_status,
        "order_status": order.status
    }
@router.put("/{customer_id}/orders/{order_id}/deliver")
def deliver_order(
    customer_id: int,
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.customer_id == customer_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.delivery_status = "Delivered"

    db.commit()

    return {
        "message": "Order Delivered Successfully",
        "order_id": order.id,
        "delivery_status": order.delivery_status
    }
@router.get("/{customer_id}/orders")
def customer_orders(
    customer_id: int,
    db: Session = Depends(get_db)
):

    orders = db.query(Order).filter(
        Order.customer_id == customer_id
    ).all()

    data = []

    for order in orders:

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            data.append({

    "order_id": order.id,

    "product": product.name,

    "quantity": item.quantity,

    "amount": item.price * item.quantity,

    "status": order.status,

    "payment_status": order.payment_status,

    "delivery_status": order.delivery_status,

    "address": order.address,

    "date": order.order_date.strftime("%d-%m-%Y")

})

    return data
@router.post("/{customer_id}/wishlist/{product_id}")
def add_to_wishlist(
    customer_id: int,
    product_id: int,
    db: Session = Depends(get_db)
):

    # Check if already exists
    existing = db.query(Wishlist).filter(
        Wishlist.customer_id == customer_id,
        Wishlist.product_id == product_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Product already in wishlist"
        )

    wishlist_item = Wishlist(
        customer_id=customer_id,
        product_id=product_id
    )

    db.add(wishlist_item)
    db.commit()

    return {
        "message": "Added to Wishlist Successfully"
    }
@router.get("/{customer_id}/wishlist")
def get_wishlist(
    customer_id: int,
    db: Session = Depends(get_db)
):

    wishlist = db.query(Wishlist).filter(
        Wishlist.customer_id == customer_id
    ).all()

    data = []

    for item in wishlist:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if product:

            data.append({

                "id": product.id,

                "name": product.name,

                "description": product.description,

                "price": product.price,

                "stock": product.stock

            })

    return data
@router.get("/{customer_id}/profile", response_model=CustomerResponse)
def customer_profile(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer
# ----------------------------
# Product Recommendations
# ----------------------------
@router.get("/{customer_id}/recommendations")
def recommend_products(
    customer_id: int,
    db: Session = Depends(get_db)
):

    # Get all orders of this customer
    orders = db.query(Order).filter(
        Order.customer_id == customer_id
    ).all()

    purchased_categories = []

    purchased_products = []

    # Find purchased products and their categories
    for order in orders:

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            if product:

                purchased_categories.append(product.category_id)
                purchased_products.append(product.id)

    # If customer has never ordered anything
    if len(purchased_categories) == 0:

        recommendations = db.query(Product).limit(6).all()

    else:

        favourite_category = max(
            set(purchased_categories),
            key=purchased_categories.count
        )

        recommendations = db.query(Product).filter(
            Product.category_id == favourite_category
        ).limit(6).all()

        if len(recommendations) == 0:
            recommendations = db.query(Product).limit(6).all()

    return recommendations
@router.put("/{customer_id}/profile")
def update_customer_profile(
    customer_id: int,
    data: dict,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if "full_name" in data:
        customer.full_name = data["full_name"]

    if "email" in data:
        customer.email = data["email"]

    if "phone" in data:
        customer.phone = data["phone"]

    if "address" in data:
        customer.address = data["address"]

    if "password" in data:
        customer.password = data["password"]

    db.commit()

    db.refresh(customer)

    return {
        "message": "Profile updated successfully"
    }