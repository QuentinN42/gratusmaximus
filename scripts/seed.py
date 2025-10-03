#!/bin/env python
import uuid

from maximus.database.migrations import get_session_maker
from maximus.database.schemas import DBKeys
from maximus.database.upsert import upsert
from sqlalchemy.orm import Session


def main(db: Session) -> None:
    upsert(db, DBKeys(id=uuid.UUID(int=1), name='Dev 1'))
    db.commit()


if __name__ == '__main__':
    maker = get_session_maker()
    session: Session = maker()
    try:
        main(session)
    finally:
        session.close()
