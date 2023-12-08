from typing import Callable
import random
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Summary
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add prometheus asgi middleware to route /metrics requests
metrics_app: Callable = make_asgi_app()
app.mount("/metrics/", metrics_app)


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")


@REQUEST_TIME.time()
@app.get("/v1/users")
def get_users() -> list[str]:
    time.sleep(random.random())
    return ["user-1", "user-2", "user-3"]


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
