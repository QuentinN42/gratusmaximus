import logging

from fastapi import FastAPI, HTTPException
from models import Event
from pydantic import BaseModel

logger = logging.getLogger(__name__)
app = FastAPI()

STORAGE = None


class HealthResult(BaseModel):
    healthy: bool


class StorageStatus(BaseModel):
    stored: bool = True


@app.get("/health")
def healthcheck() -> HealthResult:
    return HealthResult(healthy=True)


@app.post(
    "/v1/push",
    responses={
        409: {"model": None, "description": "Unable to insert."},
        501: {"model": None, "description": "Not implemented."},
    },
)
def data_v1(event: Event) -> StorageStatus:
    logger.info("Received event %s", event)
    if not STORAGE:
        raise HTTPException(status_code=501)

    return StorageStatus()
