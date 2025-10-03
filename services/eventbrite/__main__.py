from sdk.gratus import run_and_send
from sdk.models import Event
from services.eventbrite.parser import parse_response
from services.eventbrite.scrapper import get_data


def main() -> list[Event]:
    return parse_response(get_data())


if __name__ == "__main__":
    run_and_send(main())
