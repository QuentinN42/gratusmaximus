import logging

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.responses import PlainTextResponse

from sdk.models import Event, HealthResult, StorageStatus
from services.maximus.database.inject import Session, get_session
from services.maximus.database.schemas import DBEvent
from services.maximus.database.upsert import upsert
from services.maximus.ics import ics_from_db
from services.maximus.security import auth

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
            "description": "API key is required",
        },
        status.HTTP_409_CONFLICT: {
            "model": None,
            "description": "Unable to insert data.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": None,
            "description": "Invalid request.",
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
    gratter: str = Security(auth),
) -> StorageStatus:
    if not gratter:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )

    logger.info("Received event %s", event)
    if not db:
        raise HTTPException(status_code=501)

    try:
        to_add = DBEvent.from_model(event)
        to_add.gratter = gratter
        added = upsert(db, to_add)
        db.commit()
        return StorageStatus(id=added.id)
    except Exception as e:
        logger.error("Failed to insert event %s", event)
        logger.exception(e)
        raise HTTPException(status_code=409)


@app.get("/v1/ics", response_class=PlainTextResponse)
def ics_v1(db: Session = Depends(get_session)) -> str:
    return ics_from_db(db).to_ical().decode('utf-8')
