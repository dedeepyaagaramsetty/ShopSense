from app.database.database import SessionLocal

# Import all models so SQLAlchemy can resolve foreign keys
from app.models.admin import Admin
from app.models.vendor import Vendor
from app.models.category import Category
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem

db = SessionLocal()

# -----------------------------
# Create Customer
# -----------------------------
customer = Customer(
    full_name="Priya Sharma",
    email="priya@gmail.com",
    phone="9876543211",
    password="123456",
    address="Guntur"
)

db.add(customer)
db.commit()
db.refresh(customer)

# -----------------------------
# Create Order
# -----------------------------
order = Order(
    customer_id=customer.id,
    total_amount=74999,
    status="Completed"
)

db.add(order)
db.commit()
db.refresh(order)

# -----------------------------
# Create Order Item
# -----------------------------
order_item = OrderItem(
    order_id=order.id,
    product_id=3,   # Samsung Galaxy S24
    quantity=1,
    price=74999
)

db.add(order_item)
db.commit()

db.close()

print("Transaction created successfully!")