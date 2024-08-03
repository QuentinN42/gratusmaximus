import logging

# https://joshdimella.com/blog/filtering-fastapi-logs


class EndpointFilter(logging.Filter):
    def __init__(self, excluded_endpoints: list[str]) -> None:
        self.excluded_endpoints = excluded_endpoints

    def _contains_excluded_endpoints(self, record: logging.LogRecord) -> bool:
        return (
            record.args is not None
            and len(record.args) >= 3
            and isinstance(record.args, tuple)
            and isinstance(record.args[2], str)
            and record.args[2] in self.excluded_endpoints
        )

    def filter(self, record: logging.LogRecord) -> bool:
        return not self._contains_excluded_endpoints(record)
