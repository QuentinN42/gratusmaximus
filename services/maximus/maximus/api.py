import logging

from fastapi import Depends, FastAPI, HTTPException, Security, status
from models import Event, HealthResult, StorageStatus

from maximus.database.inject import Session, get_session
from maximus.database.schemas import DBEvent
from maximus.security import auth

logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/health")
def healthcheck() -> HealthResult:
    return HealthResult(healthy=True)


@app.post(
    "/v1/push",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "Invalid API key.",
        },
        status.HTTP_409_CONFLICT: {
            "model": None,
            "description": "Unable to insert data.",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": None,
            "description": "Unable to connect to backend service.",
        },
    },
)
def data_v1(
    event: Event,
    db: Session = Depends(get_session),
    authenticated: bool = Security(auth),
) -> StorageStatus:
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

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
