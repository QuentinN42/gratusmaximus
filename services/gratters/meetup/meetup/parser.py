import typing

from models import Event, Gratters, consitent_uuid


def parse(data: dict[str, typing.Any]) -> Event | None:
    if not data['venue']:
        return None
    if (
        data['venue']['eventVenueOptions']['feeSettings']
        and data['venue']['eventVenueOptions']['feeSettings']['amount']
    ):
        return None

    return Event(
        id=consitent_uuid(Gratters.MEETUP, data['id']),
        name=data['title'],
        date_start=data['dateTime'],
        date_end=data['endTime'],
        description=data['description'],
        location=f"{data['venue']['address']}, {data['venue']['city']}",
        url=data['eventUrl'],
        mandatory_registration=True,
    )
