import logging
from typing import TypeVar

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from services.maximus.database.schemas import Base

logger = logging.getLogger(__name__)
D = TypeVar('D', bound=Base)


def upsert(db: Session, to_add: D) -> D:
    """Add to the current transaction an upsert on the given class."""
    introspection = inspect(type(to_add))
    primary_key_name = introspection.primary_key[0].name
    primary_key = getattr(to_add, primary_key_name)
    existant = db.get(type(to_add), primary_key)

    if existant is None:
        logger.info(f"New event {primary_key}, inserting")
        db.add(to_add)
        return to_add

    logger.info(f"Updating event {primary_key}")
    for prop in introspection.iterate_properties:
        setattr(existant, prop.key, getattr(to_add, prop.key))
    return existant
