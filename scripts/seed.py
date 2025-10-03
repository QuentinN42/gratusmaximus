#!/bin/env python
import uuid

from sqlalchemy.orm import Session

from services.maximus.database.migrations import get_session_maker
from services.maximus.database.schemas import DBKeys
from services.maximus.database.upsert import upsert


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
