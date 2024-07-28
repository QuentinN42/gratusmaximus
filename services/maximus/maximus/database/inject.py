from typing import Generator

from sqlalchemy.orm import Session

from maximus.database.migrations import get_session_maker


def get_session() -> Generator[Session, None, None]:
    maker = get_session_maker()
    session: Session = maker()
    try:
        yield session
    finally:
        session.close()
