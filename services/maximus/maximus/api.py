import logging
import uuid

from fastapi import Depends, FastAPI, HTTPException
from models import Event
from pydantic import BaseModel

from maximus.database.inject import Session, get_session
from maximus.database.schemas import DBEvent

logger = logging.getLogger(__name__)
app = FastAPI()


class HealthResult(BaseModel):
    healthy: bool


class StorageStatus(BaseModel):
    stored: bool = True
    id: uuid.UUID


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
def data_v1(event: Event, db: Session = Depends(get_session)) -> StorageStatus:
    logger.info("Received event %s", event)
    if not db:
        raise HTTPException(status_code=501)

    try:
        to_add = DBEvent.from_model(event)
        db.add(to_add)
        db.commit()
        return StorageStatus(id=to_add.id)
    except Exception as e:
        logger.error("Failed to insert event %s", event)
        logger.exception(e)
        raise HTTPException(status_code=409)
