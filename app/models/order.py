from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.database.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String,
        default="Pending"
    )

    payment_method = Column(
        String,
        nullable=True
    )

    payment_status = Column(
        String,
        default="Pending"
    )

    delivery_status = Column(
        String,
        default="Processing"
    )

    address = Column(
        String,
        nullable=True
    )

    order_date = Column(
        DateTime,
        default=datetime.utcnow
    )