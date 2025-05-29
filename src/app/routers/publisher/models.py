from pydantic import BaseModel


class NotificationInfo(BaseModel):
    message: str