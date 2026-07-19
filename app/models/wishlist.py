from sqlalchemy import Column, Integer, ForeignKey
from app.database.database import Base


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    product_id = Column(Integer, ForeignKey("products.id"))