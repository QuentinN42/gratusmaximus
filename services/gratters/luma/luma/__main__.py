from checks.checks import speak_food
from gratus import run_and_send
from models import Event

from luma.fetch_one import fetch_one
from luma.get_events import get_events_ids


def main() -> list[Event]:
    res: list[Event] = []
    for _id in get_events_ids():
        try:
            evt = fetch_one(_id)
            if speak_food(evt.model_dump_json()):
                print(f'Event {evt.name} is accepted')
                res.append(evt)
            else:
                print(f'Event {evt.name} is not accepted')
        except Exception as e:
            print(f'ERROR: {e}')
    return res


if __name__ == "__main__":
    run_and_send(main())
