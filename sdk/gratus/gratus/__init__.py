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
