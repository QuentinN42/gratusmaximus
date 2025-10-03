#!/bin/env python

import uuid

from maximus.database.migrations import get_session_maker
from maximus.database.schemas import DBKeys
from sqlalchemy.orm import Session


def print_keys(db: Session) -> None:
    keys = db.query(DBKeys).all()
    if not keys:
        print("No keys in the current database")
        return
    for key in keys:
        print(f'{key.id} -> {key.name}')


def main(db: Session) -> None:
    while True:
        print("Current keys :")
        print_keys(db)
        print("")
        print("What do you want to do ?")
        print("")
        print("- Exit : exit / CRTL-D")
        print("- Add a key : add [name]")
        print("- Delete a key : del [uuid]")
        try:
            action = input()
        except EOFError:
            return
        if action == 'exit':
            return
        elif action.startswith("add "):
            name = action.removeprefix("add ")
            print(f"Creating key {name}")
            db.add(DBKeys(id=uuid.uuid4(), name=name))
            db.commit()
        elif action.startswith("del "):
            _id = action.removeprefix("del ")
            res = (
                db.query(DBKeys)
                .filter(
                    DBKeys.id == _id,
                )
                .first()
            )
            if res:
                print(f"Deleting key {_id}")
                db.delete(res)
                db.commit()
            else:
                print(f"Key {_id} not found")
        else:
            print("Unknow action ...")
        print("\n" * 3)


if __name__ == '__main__':
    maker = get_session_maker()
    session: Session = maker()
    try:
        main(session)
    finally:
        session.close()
