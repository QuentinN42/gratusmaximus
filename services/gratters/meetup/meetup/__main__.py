from checks.checks import speak_food, is_free
from gratus import run_and_send
from models import Event

from meetup.collector import collect
from meetup.gql import check
from meetup.parser import parse


def main() -> list[Event]:
    check()

    ret: list[Event] = []
    for d in collect():
        if (evt := parse(d)) is not None:
            if speak_food(evt.model_dump_json()) and is_free(evt.model_dump_json()):
                print(f'Event {evt.name} is accepted')
                ret.append(evt)
            else:
                print(f'Event {evt.name} is not accepted')

    return ret


if __name__ == "__main__":
    run_and_send(main())
