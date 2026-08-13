from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.notification import Notification


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/{user_type}/{user_id}")
def get_notifications(
    user_type: str,
    user_id: int,
    db: Session = Depends(get_db)
):

    notifications = db.query(Notification).filter(
        Notification.user_type == user_type,
        Notification.user_id == user_id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return [
        {
            "id": notification.id,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": notification.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )
        }

        for notification in notifications
    ]