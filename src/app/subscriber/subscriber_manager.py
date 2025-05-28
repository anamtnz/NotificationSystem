from app.publisher.publisher_manager import PublishersManager
from app.subscriber.models import Subscriber


class SubscribersManager:

    def __init__(self, publishers_manager: PublishersManager):
        self._publishers_manager = publishers_manager

    def register(self, subscriber: Subscriber) -> None:
        self._publishers_manager.add_subscriber(subscriber)

    def unregister(self, subscriber_id: str) -> None:
        self._publishers_manager.delete_subscriber(subscriber_id)