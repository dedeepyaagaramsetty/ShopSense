from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, product: ProductCreate):
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