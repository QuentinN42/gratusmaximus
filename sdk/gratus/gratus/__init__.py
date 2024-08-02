import os

import httpx
from models import Event, Gratters, StorageStatus

_HEALTH = 'health'
_PUSH = 'v1/push'


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

        if not self.healthy():
            print(f"[WRN] Unable to health check {self.__remote}")

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
        res = httpx.post(
            self.__remote + _PUSH,
            headers={
                'x-api-key': self.__api_key,
                'x-gratter-type': self.__gratter_type.name,
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            content=event.model_dump_json(),
        )
        res.raise_for_status()
        result = StorageStatus.model_validate_json(res.content)
        print(
            f'[INF] Stored {event.name} with id {result.id}. Link {event.url}'
        )

    def healthy(self) -> bool:
        res = httpx.get(self.__remote + _HEALTH)
        return res.status_code == httpx.codes.OK
