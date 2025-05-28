from pydantic import BaseModel


class SubscriberInfo(BaseModel):
    id: str
    name: str | None = None
    url: str