from fastapi import FastAPI
from app.routers.transaction import router as transaction_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers.category import router as category_router
from app.routers.vendor import router as vendor_router
from app.routers.admin import router as admin_router
from app.database.database import Base, engine
from app.routers.product import router as product_router
# Import all models
from app.models.admin import Admin
from app.models.vendor import Vendor
from app.models.customer import Customer
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ShopSense API",
    description="Multi-Vendor E-Commerce Analytics Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(transaction_router)
app.include_router(vendor_router)
app.include_router(admin_router)
app.include_router(product_router)
app.include_router(category_router)
@app.get("/")
def home():
    return {
        "message": "Welcome to ShopSense!"
    }