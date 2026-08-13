import random
from datetime import datetime, timedelta

from app.database.database import SessionLocal, Base, engine

# Import every model so SQLAlchemy knows all tables
from app.models.vendor import Vendor
from app.models.category import Category
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.wishlist import Wishlist
from app.models.notification import Notification

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

NUM_VENDORS = 15
NUM_CATEGORIES = 10
NUM_PRODUCTS = 100
NUM_CUSTOMERS = 200
NUM_ORDERS = 1000

random.seed(42)

# --------------------------------------------------
# SAMPLE DATA
# --------------------------------------------------

VENDOR_NAMES = [
    ("Tech World", "Arjun"),
    ("Smart Electronics", "Ravi"),
    ("Digital Hub", "Kiran"),
    ("Mobile Planet", "Suresh"),
    ("Laptop Zone", "Vikram"),
    ("Fashion Hub", "Priya"),
    ("Style Street", "Ananya"),
    ("Trend Store", "Sneha"),
    ("Fresh Mart", "Rahul"),
    ("Grocery Mart", "Karthik"),
    ("Home Essentials", "Divya"),
    ("Beauty Basket", "Meena"),
    ("Sports World", "Akhil"),
    ("Book House", "Varun"),
    ("Daily Needs", "Pooja"),
]

CATEGORIES = [
    ("Mobiles", "Smartphones and mobile accessories"),
    ("Laptops", "Laptops and computing devices"),
    ("Electronics", "Electronic gadgets and accessories"),
    ("Fashion", "Clothing and fashion products"),
    ("Grocery", "Daily grocery and food products"),
    ("Home", "Home and kitchen essentials"),
    ("Beauty", "Beauty and personal care products"),
    ("Sports", "Sports and fitness products"),
    ("Books", "Books and educational materials"),
    ("Accessories", "Lifestyle and general accessories"),
]

PRODUCT_NAMES = [
    "Samsung Galaxy A55",
    "iPhone 15",
    "OnePlus Nord CE",
    "Redmi Note 14",
    "Realme 13 Pro",
    "Vivo V30",
    "Nothing Phone 2",
    "Google Pixel 8",
    "Samsung Galaxy S24",
    "OnePlus 12",

    "HP Pavilion 15",
    "Dell Inspiron 15",
    "Lenovo IdeaPad Slim",
    "ASUS VivoBook",
    "Acer Aspire 5",
    "MacBook Air M2",
    "MacBook Air M3",
    "HP Victus",
    "Lenovo LOQ",
    "ASUS TUF Gaming",

    "Sony Headphones",
    "JBL Bluetooth Speaker",
    "Boat Earbuds",
    "Apple AirPods",
    "Mi Smart TV",
    "Sony Bravia TV",
    "Canon Printer",
    "Logitech Keyboard",
    "Dell Monitor",
    "Samsung Monitor",

    "Men's T-Shirt",
    "Women's Kurti",
    "Denim Jeans",
    "Formal Shirt",
    "Cotton Saree",
    "Sports Shoes",
    "Casual Shoes",
    "Hoodie",
    "Jacket",
    "Handbag",

    "Basmati Rice",
    "Wheat Flour",
    "Cooking Oil",
    "Sugar",
    "Tea Powder",
    "Coffee Powder",
    "Biscuits",
    "Dry Fruits",
    "Pasta",
    "Breakfast Cereal",

    "Mixer Grinder",
    "Electric Kettle",
    "Non-Stick Pan",
    "Dinner Set",
    "Water Bottle",
    "Storage Container",
    "Bedsheet",
    "Curtains",
    "Table Lamp",
    "Wall Clock",

    "Face Wash",
    "Moisturizer",
    "Shampoo",
    "Conditioner",
    "Sunscreen",
    "Lip Balm",
    "Perfume",
    "Body Lotion",
    "Hair Oil",
    "Face Serum",

    "Yoga Mat",
    "Dumbbells",
    "Cricket Bat",
    "Football",
    "Badminton Racket",
    "Tennis Ball",
    "Skipping Rope",
    "Gym Gloves",
    "Cycling Helmet",
    "Resistance Bands",

    "Python Programming",
    "Data Structures",
    "Machine Learning Basics",
    "Database Systems",
    "Computer Networks",
    "Operating Systems",
    "Artificial Intelligence",
    "Web Development",
    "Deep Learning",
    "Software Engineering",

    "Backpack",
    "Wallet",
    "Watch",
    "Sunglasses",
    "Travel Bag",
    "Water Flask",
    "Keychain",
    "Umbrella",
    "Phone Case",
    "Laptop Bag",
]

PAYMENT_METHODS = [
    "UPI",
    "Card",
    "Cash on Delivery",
    "Net Banking",
]

DELIVERY_STATUSES = [
    "Processing",
    "Shipped",
    "Delivered",
]

# --------------------------------------------------
# DATABASE SESSION
# --------------------------------------------------

db = SessionLocal()

try:

    print("\n========================================")
    print("      ShopSense CLEAN RESEED")
    print("========================================\n")

    # --------------------------------------------------
    # 1. CLEAR EXISTING DATA
    # --------------------------------------------------

    print("Clearing existing data...")

    # Delete in dependency order
    db.query(Wishlist).delete()
    db.query(Notification).delete()
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(Product).delete()
    db.query(Customer).delete()
    db.query(Vendor).delete()
    db.query(Category).delete()

    db.commit()

    print("Existing data cleared.\n")

    # --------------------------------------------------
    # 2. CREATE CATEGORIES
    # --------------------------------------------------

    print("Creating categories...")

    categories = []

    for name, description in CATEGORIES:

        category = Category(
            name=name,
            description=description
        )

        db.add(category)
        categories.append(category)

    db.commit()

    for category in categories:
        db.refresh(category)

    print(f"Created {len(categories)} categories.")

    # --------------------------------------------------
    # 3. CREATE VENDORS
    # --------------------------------------------------

    print("Creating vendors...")

    vendors = []

    for i, (business_name, owner_name) in enumerate(
        VENDOR_NAMES[:NUM_VENDORS],
        start=1
    ):

        vendor = Vendor(
            business_name=business_name,
            owner_name=owner_name,
            email=f"vendor{i}@shopsense.com",
            phone=f"987650{i:04d}",
            password="Vendor@123",
            status="Approved"
        )

        db.add(vendor)
        vendors.append(vendor)

    db.commit()

    for vendor in vendors:
        db.refresh(vendor)

    print(f"Created {len(vendors)} approved vendors.")

    # --------------------------------------------------
    # 4. CREATE PRODUCTS
    # --------------------------------------------------

    print("Creating products...")

    products = []

    for i in range(NUM_PRODUCTS):

        vendor = random.choice(vendors)
        category = random.choice(categories)

        base_price = random.randint(300, 80000)

        product = Product(
            name=PRODUCT_NAMES[i],
            description=f"High-quality {PRODUCT_NAMES[i]} available from {vendor.business_name}.",
            price=base_price,
            stock=random.randint(10, 100),
            category_id=category.id,
            vendor_id=vendor.id
        )

        db.add(product)
        products.append(product)

    db.commit()

    for product in products:
        db.refresh(product)

    print(f"Created {len(products)} products.")

    # --------------------------------------------------
    # 5. CREATE CUSTOMERS
    # --------------------------------------------------

    print("Creating customers...")

    customers = []

    first_names = [
        "Aarav",
        "Aditya",
        "Ananya",
        "Arjun",
        "Diya",
        "Ishaan",
        "Kavya",
        "Meera",
        "Nikhil",
        "Rahul",
        "Riya",
        "Saanvi",
        "Sahil",
        "Sneha",
        "Varun",
        "Vijay",
        "Pooja",
        "Karthik",
        "Priya",
        "Rohan",
    ]

    cities = [
        "Guntur",
        "Vijayawada",
        "Hyderabad",
        "Chennai",
        "Bangalore",
        "Visakhapatnam",
        "Pune",
        "Mumbai",
        "Delhi",
        "Kolkata",
    ]

    for i in range(1, NUM_CUSTOMERS + 1):

        name = random.choice(first_names) + f" {i}"

        customer = Customer(
            full_name=name,
            email=f"customer{i}@shopsense.com",
            phone=f"90000{i:05d}",
            password="Customer@123",
            address=f"{random.randint(1, 999)} Main Road, {random.choice(cities)}"
        )

        db.add(customer)
        customers.append(customer)

    db.commit()

    for customer in customers:
        db.refresh(customer)

    print(f"Created {len(customers)} customers.")

    # --------------------------------------------------
    # 6. CREATE ORDERS
    # --------------------------------------------------

    print("Creating orders...")

    now = datetime.utcnow()

    completed_count = 0
    pending_count = 0
    order_items_created = 0

    for order_number in range(NUM_ORDERS):

        customer = random.choice(customers)

        # Spread orders over the previous 6 months
        days_ago = random.randint(0, 180)

        order_date = now - timedelta(
            days=days_ago,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        # Around 90% completed so analytics has plenty of revenue
        if random.random() < 0.90:

            status = "Completed"
            payment_status = "Paid"
            completed_count += 1

        else:

            status = "Pending"
            payment_status = "Pending"
            pending_count += 1

        payment_method = random.choice(PAYMENT_METHODS)

        if payment_status == "Pending":
            payment_method = random.choice(
                ["Cash on Delivery", "UPI"]
            )

        delivery_status = random.choice(
            DELIVERY_STATUSES
        )

        # Create between 1 and 3 products in each order
        number_of_items = random.randint(1, 3)

        selected_products = random.sample(
            products,
            number_of_items
        )

        total_amount = 0

        order = Order(
            customer_id=customer.id,
            total_amount=0,
            status=status,
            payment_method=payment_method,
            payment_status=payment_status,
            delivery_status=delivery_status,
            address=customer.address,
            order_date=order_date
        )

        db.add(order)
        db.flush()

        for product in selected_products:

            quantity = random.randint(1, 3)

            # Don't make stock negative
            if product.stock < quantity:
                quantity = max(1, product.stock)

            if quantity <= 0:
                continue

            item_price = product.price

            total_amount += item_price * quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=item_price
            )

            db.add(order_item)

            # Reduce stock
            product.stock -= quantity

            order_items_created += 1

        order.total_amount = round(total_amount, 2)

    db.commit()

    print(f"Created {NUM_ORDERS} orders.")
    print(f"Completed orders: {completed_count}")
    print(f"Pending orders: {pending_count}")
    print(f"Created order items: {order_items_created}")

    # --------------------------------------------------
    # 7. CREATE WISHLISTS
    # --------------------------------------------------

    print("Creating wishlist records...")

    wishlist_count = 0

    for customer in random.sample(
        customers,
        min(150, len(customers))
    ):

        wishlist_products = random.sample(
            products,
            random.randint(1, 5)
        )

        for product in wishlist_products:

            wishlist = Wishlist(
                customer_id=customer.id,
                product_id=product.id
            )

            db.add(wishlist)

            wishlist_count += 1

    db.commit()

    print(f"Created {wishlist_count} wishlist records.")

    # --------------------------------------------------
    # 8. CREATE NOTIFICATIONS
    # --------------------------------------------------

    print("Creating notifications...")

    notification_count = 0

    for customer in random.sample(
        customers,
        min(50, len(customers))
    ):

        notification = Notification(
            user_type="customer",
            user_id=customer.id,
            message="Welcome to ShopSense! Explore our marketplace."
        )

        db.add(notification)

        notification_count += 1

    for vendor in vendors:

        notification = Notification(
            user_type="vendor",
            user_id=vendor.id,
            message="Your ShopSense vendor account is approved."
        )

        db.add(notification)

        notification_count += 1

    db.commit()

    print(f"Created {notification_count} notifications.")

    # --------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------

    print("\n========================================")
    print("        SEEDING COMPLETED")
    print("========================================")

    print(f"Vendors       : {db.query(Vendor).count()}")
    print(f"Categories    : {db.query(Category).count()}")
    print(f"Products      : {db.query(Product).count()}")
    print(f"Customers     : {db.query(Customer).count()}")
    print(f"Orders        : {db.query(Order).count()}")
    print(f"Order Items   : {db.query(OrderItem).count()}")
    print(f"Wishlist      : {db.query(Wishlist).count()}")
    print(f"Notifications : {db.query(Notification).count()}")

    completed_revenue = sum(
        order.total_amount
        for order in db.query(Order).filter(
            Order.status == "Completed"
        ).all()
    )

    print(
        f"\nCompleted Revenue : ₹{completed_revenue:,.2f}"
    )

    print("\n========================================")
    print(" ShopSense is ready for milestone testing!")
    print("========================================\n")

except Exception as e:

    db.rollback()

    print("\n❌ SEEDING FAILED")
    print("Error:", e)

    raise

finally:

    db.close()