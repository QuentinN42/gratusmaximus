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


class Gratter:
    """A gratter is an object that can send some results to maximus."""

    def __init__(
        self,
        remote: str,
        api_key: str,
        gratter_type: str,
    ) -> None:
        self.__remote = remote
        self.__api_key = api_key
        self.__gratter_type = gratter_type

    def send(self, result: str) -> None:
        """Send the result to maximus."""
        pass
