from gratus import Gratter
from models import Gratters

from eventbrite.parser import parse_response
from eventbrite.scrapper import get_data


def main() -> None:
    print("Eventbrite scrapping started!")

    gratter = Gratter.from_env(Gratters.EVENTBRITE)
    print("Gratter init success")

    events = parse_response(get_data())
    print(f"Found : {len(events)} events")

    for event in events:
        gratter.send(event)

    print("Done")


if __name__ == "__main__":
    main()
