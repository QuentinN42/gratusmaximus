import logging

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from services.maximus.database.inject import Session, get_session
from services.maximus.database.schemas import DBKeys

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def auth(
    api_key_header: str = Security(api_key_header),
    db: Session = Depends(get_session),
) -> str:
    """Validate apikey against the DB."""
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )

    logger.debug('Validating API key')

    res = (
        db.query(DBKeys)
        .filter(
            DBKeys.id == api_key_header,
        )
        .first()
    )
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )

    return res.name
