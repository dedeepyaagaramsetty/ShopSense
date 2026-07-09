from app.database.database import SessionLocal

from app.models.vendor import Vendor
from app.models.category import Category
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem

db = SessionLocal()

# -------------------------
# Categories
# -------------------------
categories = [
    ("Mobiles", "Smartphones"),
    ("Laptops", "Laptop Computers"),
    ("Fashion", "Clothing"),
    ("Grocery", "Daily Essentials")
]

for name, desc in categories:
    if not db.query(Category).filter(Category.name == name).first():
        db.add(Category(name=name, description=desc))

db.commit()

# -------------------------
# Vendors
# -------------------------
vendors = [
    ("Tech World", "Suresh", "suresh@gmail.com", "9876500001", "123", "Approved"),
    ("Fashion Hub", "Priya", "priya.vendor@gmail.com", "9876500002", "123", "Pending"),
    ("Grocery Mart", "Akash", "akash@gmail.com", "9876500003", "123", "Approved")
]

for business, owner, email, phone, password, status in vendors:
    if not db.query(Vendor).filter(Vendor.email == email).first():
        db.add(Vendor(
            business_name=business,
            owner_name=owner,
            email=email,
            phone=phone,
            password=password,
            status=status
        ))

db.commit()

# -------------------------
# Customers
# -------------------------
customers = [
    ("Rahul Kumar", "rahul.customer@gmail.com", "9991111111", "123", "Guntur"),
    ("Sneha Reddy", "sneha@gmail.com", "9991111112", "123", "Hyderabad"),
    ("Arjun Rao", "arjun@gmail.com", "9991111113", "123", "Vijayawada"),
    ("Neha Patel", "neha@gmail.com", "9991111114", "123", "Chennai")
]

for name, email, phone, password, address in customers:
    if not db.query(Customer).filter(Customer.email == email).first():
        db.add(Customer(
            full_name=name,
            email=email,
            phone=phone,
            password=password,
            address=address
        ))

db.commit()

# -------------------------
# Get IDs
# -------------------------
mobile = db.query(Category).filter(Category.name == "Mobiles").first()
laptop = db.query(Category).filter(Category.name == "Laptops").first()
fashion = db.query(Category).filter(Category.name == "Fashion").first()
grocery = db.query(Category).filter(Category.name == "Grocery").first()

vendors = db.query(Vendor).all()

# -------------------------
# Products
# -------------------------
products = [
    ("iPhone 15", "Apple Smartphone", 79999, 25, mobile.id, vendors[0].id),
    ("Dell Inspiron", "Dell Laptop", 65000, 18, laptop.id, vendors[0].id),
    ("HP Pavilion", "HP Laptop", 72000, 12, laptop.id, vendors[1].id),
    ("Men T-Shirt", "Cotton T-Shirt", 799, 120, fashion.id, vendors[1].id),
    ("Rice Bag 25kg", "Premium Rice", 1499, 45, grocery.id, vendors[2].id),
    ("Sunflower Oil", "1L Oil", 210, 80, grocery.id, vendors[2].id)
]

for p in products:
    if not db.query(Product).filter(Product.name == p[0]).first():
        db.add(Product(
            name=p[0],
            description=p[1],
            price=p[2],
            stock=p[3],
            category_id=p[4],
            vendor_id=p[5]
        ))

db.commit()

# -------------------------
# Orders
# -------------------------
customers = db.query(Customer).all()

if db.query(Order).count() <= 1:

    order1 = Order(customer_id=customers[0].id, total_amount=79999, status="Completed")
    order2 = Order(customer_id=customers[1].id, total_amount=65000, status="Completed")
    order3 = Order(customer_id=customers[2].id, total_amount=1499, status="Pending")

    db.add_all([order1, order2, order3])
    db.commit()

    db.refresh(order1)
    db.refresh(order2)
    db.refresh(order3)

    products = db.query(Product).all()

    db.add_all([
        OrderItem(order_id=order1.id, product_id=products[0].id, quantity=1, price=79999),
        OrderItem(order_id=order2.id, product_id=products[1].id, quantity=1, price=65000),
        OrderItem(order_id=order3.id, product_id=products[4].id, quantity=1, price=1499)
    ])

    db.commit()

db.close()

print("Sample data inserted successfully!")