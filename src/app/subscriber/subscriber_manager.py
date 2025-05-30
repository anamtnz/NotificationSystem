from app.publisher.publisher_manager import PublisherManager
from app.subscriber.models import Subscriber
from app.utils.logger_decorator import logger_decorator


class SubscriberManager:

    def __init__(self, publisher_manager: PublisherManager):
        self._publisher_manager = publisher_manager

    @logger_decorator
    def register(self, subscriber: Subscriber) -> None:
        self._publisher_manager.add_subscriber(subscriber)

    @logger_decorator
    def unregister(self, subscriber_id: str) -> None:
        self._publisher_manager.delete_subscriber(subscriber_id)