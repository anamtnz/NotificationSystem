import logging.config

import uvicorn
from fastapi import FastAPI

from app.routers.publisher import publisher
from app.routers.subscriber import subscriber

app = FastAPI()
app.include_router(subscriber.router)
app.include_router(publisher.router)


def main():
    logging.config.fileConfig("logging.cfg")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
