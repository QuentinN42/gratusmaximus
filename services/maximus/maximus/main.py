from os import getenv

from uvicorn import run

from maximus.api import app


def main():
    port = int(getenv("PORT", "8080"))
    run(
        app=app,
        host="0.0.0.0",
        port=port,
    )
