import logging

from app.publisher.models import Notification
from app.subscriber.models import Subscriber, SubscriberAlreadyExistsException, SubscriberDoesNotExistsException
from httpx import post

logger = logging.getLogger(__name__)


class PublishersManager:

    def __init__(self):
        self.subscribers: dict[str, Subscriber] = {}

    def add_subscriber(self, subscriber: Subscriber) -> None:
        if self.subscribers.get(subscriber.id):
            raise SubscriberAlreadyExistsException(subscriber.id)
        self.subscribers[subscriber.id] = subscriber

    def delete_subscriber(self, subscriber_id: str) -> None:
        if not self.subscribers.get(subscriber_id):
            raise SubscriberDoesNotExistsException(subscriber_id)
        self.subscribers.pop(subscriber_id)

    def get_subscribers(self) -> list[Subscriber]:
        return [subscriber for subscriber in self.subscribers.values()]

    def send_notification(self, notification: Notification) -> list[str]:
        subscribers_not_notified = []
        for subscriber in self.get_subscribers():
            try:
                post(subscriber.url, json=notification.model_dump())
            except Exception as e:
                logger.exception(f"Error sending notification to subscriber {subscriber.id}: {e}")
                subscribers_not_notified.append(subscriber.id)
        return subscribers_not_notified
