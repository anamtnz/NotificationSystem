import logging

from fastapi import APIRouter, HTTPException
from app.dependencies import get_publishers_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publisher", tags=["publisher"])

manager = get_publishers_manager()


@router.get("/subscribers")
def get_subscribers():
    try:
        return manager.get_subscribers()
    except Exception as e:
        logger.exception(f"Exception registering subscriber: {e}")
        raise HTTPException(status_code=500, detail=str(e))
