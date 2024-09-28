from gratus import run_and_send
from models import Event

from meetup.gql import check


def main() -> list[Event]:
    check()
    return []


if __name__ == "__main__":
    run_and_send(main())
