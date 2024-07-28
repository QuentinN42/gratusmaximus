from pydantic import AwareDatetime
from pydantic.main import BaseModel


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
