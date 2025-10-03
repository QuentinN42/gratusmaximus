import logging
import os
import sys
from pathlib import Path
from subprocess import PIPE, Popen

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_alembic_dir = Path(__file__).parent.parent.parent.parent

logger = logging.getLogger(__name__)

metadata = sqlalchemy.MetaData()
__session_maker: sessionmaker | None = None


def run_migrations() -> None:
    logger.info('Running alembic migrations')

    res = Popen(
        [  # noqa: S603, S607
            'alembic',
            'upgrade',
            'head',
        ],
        env=os.environ.copy(),
        stdin=PIPE,
        cwd=_alembic_dir,
    ).wait()
    if res != 0:
        logger.error('Failed to run alembic migrations')
        sys.exit(res)


def get_session_maker() -> sessionmaker:
    global __session_maker
    if __session_maker is not None:
        return __session_maker

    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        logger.error('DATABASE_URL is not set')
        sys.exit(1)

    engine = create_engine(
        DATABASE_URL,
    )
    __session_maker = sessionmaker(bind=engine)
    return __session_maker
