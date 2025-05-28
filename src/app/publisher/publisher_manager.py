from app.subscriber.models import Subscriber, SubscriberAlreadyExistsException, SubscriberDoesNotExistsException


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
