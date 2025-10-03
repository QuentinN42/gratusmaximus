import logging
from os import getenv

from uvicorn import run

from services.maximus.api import app
from services.maximus.database.migrations import run_migrations
from services.maximus.logs import EndpointFilter

logger = logging.getLogger(__name__)


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
