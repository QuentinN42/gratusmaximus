import os

import httpx
from models import Event, Gratters


class Gratter:
    """A gratter is an object that can send some results to maximus."""

    def __init__(
        self,
        remote: str,
        api_key: str,
        gratter_type: Gratters,
    ) -> None:
        self.__remote = remote
        self.__api_key = api_key
        self.__gratter_type = gratter_type

    @classmethod
    def from_env(
        cls,
        gratter_type: Gratters,
    ) -> 'Gratter':
        url = os.getenv('MAXIMUS_URL')
        if not url:
            raise EnvironmentError('MAXIMUS_URL needed')
        key = os.getenv('MAXIMUS_API_KEY')
        if not key:
            raise EnvironmentError('MAXIMUS_API_KEY needed')
        return cls(
            remote=url,
            api_key=key,
            gratter_type=gratter_type,
        )

    def send(self, event: Event) -> None:
        """Send the result to maximus."""
        httpx.post(
            self.__remote,
            headers={
                'x-api-key': self.__api_key,
                'x-gratter-type': self.__gratter_type.name,
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            content=event.model_dump_json(),
        )
