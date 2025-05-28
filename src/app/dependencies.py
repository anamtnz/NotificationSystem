from functools import lru_cache

from app.publisher.publisher_manager import PublishersManager
from app.subscriber.subscriber_manager import SubscribersManager


@lru_cache
def get_publishers_manager() -> PublishersManager:
    return PublishersManager()


@lru_cache
def get_subscribers_manager() -> SubscribersManager:
    return SubscribersManager(publishers_manager=get_publishers_manager())
