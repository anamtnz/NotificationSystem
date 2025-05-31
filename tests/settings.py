from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    subscriber_port: int = 9000



settings = Settings()