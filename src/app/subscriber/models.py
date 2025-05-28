from pydantic import BaseModel


class Subscriber(BaseModel):
    id: str
    name: str | None = None
    url: str

class SubscriberAlreadyExistsException(Exception):
    """ A subscribers with this info already exists """
    def __init__(self, subscriber_id: str) -> None:
        self.subscriber_id = subscriber_id

    def __str__(self) -> str:
        return f'Subscriber {self.subscriber_id} already exists'


class SubscriberDoesNotExistsException(Exception):
    """ A subscribers with this info does not exist """

    def __init__(self, subscriber_id: str) -> None:
        self.subscriber_id = subscriber_id

    def __str__(self) -> str:
        return f'Subscriber {self.subscriber_id} does not exist'