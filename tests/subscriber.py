import uvicorn
from fastapi import FastAPI, Request

from settings import settings

app = FastAPI()


@app.post("/notify")
async def receive_notification(notification: Request):
    data = await notification.json()
    print(data)


def main():
    uvicorn.run("subscriber:app", host="0.0.0.0", port=settings.subscriber_port)


if __name__ == "__main__":
    main()
