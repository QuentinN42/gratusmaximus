import uuid
from enum import Enum, auto

from pydantic import AwareDatetime
from pydantic.main import BaseModel


class HealthResult(BaseModel):
    healthy: bool


class StorageStatus(BaseModel):
    stored: bool = True
    id: uuid.UUID


class Event(BaseModel):
    id: uuid.UUID
    """An unique idenfier of the event for deduplication purposes."""
    name: str
    """The name of the event"""
    date_start: AwareDatetime
    """The start of the event"""
    date_end: AwareDatetime
    """The end of the event"""
    description: str
    """A long description of the event"""
    location: str
    url: str
    """The source url of the event to register"""
    mandatory_registration: bool
    """If you need to be registred to be accepted at the event"""


class Gratters(Enum):
    MEETUP = auto()
    EVENTBRITE = auto()


ALL_GRATTERS = {x.name for x in Gratters}


def consitent_uuid(gratter: Gratters, context: str) -> uuid.UUID:
    """Return always the same UUID given the same context."""
    return uuid.uuid5(uuid.UUID(int=gratter.value), context)
