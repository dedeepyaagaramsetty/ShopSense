from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/add", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,
        vendor_id=product.vendor_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
@router.get("/vendor/{vendor_id}")
def get_vendor_products(vendor_id: int, db: Session = Depends(get_db)):

    products = db.query(Product).filter(
        Product.vendor_id == vendor_id
    ).all()

    return products
@router.put("/update/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.stock = updated_product.stock
    product.category_id = updated_product.category_id
    product.vendor_id = updated_product.vendor_id

    db.commit()
    db.refresh(product)

    return product
@router.delete("/delete/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}