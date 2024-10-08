import logging
from os import getenv

from uvicorn import run

from maximus.api import app
from maximus.database.migrations import run_migrations
from maximus.logs import EndpointFilter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def start_server(port: int) -> None:
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter(['/health']))
    logger.info(f"Starting server on http://0.0.0.0:{port}/")
    run(
        app=app,
        host="0.0.0.0",
        port=port,
    )


def main():
    run_migrations()
    start_server(port=int(getenv("PORT", "8080")))
