#!/bin/env python

import argparse
import uuid

from sqlalchemy.orm import Session

from services.maximus.database.migrations import get_session_maker
from services.maximus.database.schemas import DBKeys


def main(db: Session, name: str) -> None:
    key = (
        db.query(DBKeys)
        .filter(
            DBKeys.name == name,
        )
        .first()
    )
    if key is None:
        key = DBKeys(id=uuid.uuid4(), name=name)
        db.add(key)
        db.commit()
    print(key.id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n', type=str, help='Name of the key to add')
    ns = parser.parse_args()
    name = ns.name
    assert isinstance(name, str) and name, "Name is required"

    maker = get_session_maker()
    session: Session = maker()
    try:
        main(session, name)
    finally:
        session.close()
