from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_type = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    is_read = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )