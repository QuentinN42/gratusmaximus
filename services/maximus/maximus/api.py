import logging

from fastapi import Depends, FastAPI, Header, HTTPException, Security, status
from models import ALL_GRATTERS, Event, HealthResult, StorageStatus

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
    authenticated: bool = Security(auth),
    gratter: str | None = Header(default=None, alias='x-gratter-type'),
) -> StorageStatus:
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    if not gratter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing x-gratter-type header",
        )
    if gratter not in ALL_GRATTERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gratter type not in list : {ALL_GRATTERS}",
        )

    logger.info("Received event %s", event)
    if not db:
        raise HTTPException(status_code=501)

    try:
        to_add = DBEvent.from_model(event)
        to_add.gratter = gratter
        db.add(to_add)
        db.commit()
        return StorageStatus(id=to_add.id)
    except Exception as e:
        logger.error("Failed to insert event %s", event)
        logger.exception(e)
        raise HTTPException(status_code=409)
