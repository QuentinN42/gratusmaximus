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
