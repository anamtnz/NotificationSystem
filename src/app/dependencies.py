from functools import lru_cache

from app.publisher.publisher_manager import PublisherManager
from app.subscriber.subscriber_manager import SubscriberManager


@lru_cache
def get_publishers_manager() -> PublisherManager:
    return PublisherManager()


@lru_cache
def get_subscribers_manager() -> SubscriberManager:
    return SubscriberManager(publisher_manager=get_publishers_manager())
