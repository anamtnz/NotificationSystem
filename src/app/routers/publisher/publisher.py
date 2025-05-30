import logging

from fastapi import APIRouter, HTTPException
from app.dependencies import get_publisher_manager
from app.publisher.models import Notification
from app.routers.publisher.models import NotificationInfo
from app.subscriber.models import Subscriber

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publisher", tags=["publisher"])

manager = get_publisher_manager()


@router.get("/subscribers")
def get_subscribers() -> list[Subscriber]:
    try:
        return manager.get_subscribers()
    except Exception as e:
        logger.exception(f"Exception registering subscriber: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send_notification")
def send_notification(notification: NotificationInfo) -> list[str]:
    try:
        return manager.send_notification(_to_notification(notification))
    except Exception as e:
        logger.exception(f"Exception sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _to_notification(notification_info: NotificationInfo) -> Notification:
    return Notification.model_validate(notification_info.model_dump(exclude_none=True))