import logging

from fastapi import APIRouter, HTTPException

from app.routers.subscriber.models import SubscriberInfo
from app.subscriber.models import Subscriber, SubscriberAlreadyExistsException, SubscriberDoesNotExistsException
from app.dependencies import get_subscribers_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subscriber", tags=["subscriber"])

manager = get_subscribers_manager()


@router.post("/register")
def register(subscriber_info: SubscriberInfo) -> None:
    try:
        manager.register(_to_subscriber(subscriber_info))
    except SubscriberAlreadyExistsException as e:
        logger.exception(f"{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Exception registering subscriber: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/unregister/{subscriber_id}")
def unregister(subscriber_id: str) -> None:
    try:
        manager.unregister(subscriber_id)
    except SubscriberDoesNotExistsException as e:
        logger.exception(f"{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Exception unregistering subscriber: {e}")


def _to_subscriber(subscriber_info: SubscriberInfo) -> Subscriber:
    return Subscriber.model_validate(subscriber_info.model_dump(exclude_none=True))