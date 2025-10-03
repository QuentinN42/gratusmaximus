import os

import httpx

from sdk.models import Event, StorageStatus

_HEALTH = '/health'
_PUSH = '/v1/push'


class Gratter:
    """A gratter is an object that can send some results to maximus."""

    def __init__(
        self,
        remote: str,
        api_key: str,
    ) -> None:
        self.__remote = remote
        while self.__remote.endswith('/'):
            self.__remote = self.__remote[:-1]
        self.__api_key = api_key

        if not self.healthy():
            print(f"[WRN] Unable to health check {self.__remote}")

    @classmethod
    def from_env(
        cls,
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
        )

    def send(self, event: Event) -> None:
        """Send the result to maximus."""
        res = httpx.post(
            self.__remote + _PUSH,
            headers={
                'x-api-key': self.__api_key,
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


def run_and_send(events: list[Event]) -> None:
    """Simpe helper to run and send events.

    ```python
    from sdk.models import Event

    def main() -> list[Event]:
        return []

    if __name__ == "__main__":
        run_and_send(main())
    ```
    """
    gratter = Gratter.from_env()
    print("Gratter init success")

    print(f"Found : {len(events)} events")

    for event in events:
        gratter.send(event)

    print("Done")
