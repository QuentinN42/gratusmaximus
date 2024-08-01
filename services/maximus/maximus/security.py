import logging

from fastapi import Depends, Security
from fastapi.security import APIKeyHeader

from maximus.database.inject import Session, get_session
from maximus.database.schemas import DBKeys

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def auth(
    api_key_header: str = Security(api_key_header),
    db: Session = Depends(get_session),
) -> bool:
    """Validate apikey against the DB."""
    if not api_key_header:
        return False

    logger.debug('Validating API key')

    res = (
        db.query(DBKeys)
        .filter(
            DBKeys.id == api_key_header,
        )
        .first()
    )
    return res is not None
