import datetime

from models import Event
from pydantic import BaseModel
from pytz import timezone
from pytz.tzinfo import DstTzInfo, StaticTzInfo


class Address(BaseModel):
    localized_address_display: str


class PrimaryVenue(BaseModel):
    address: Address


class EBEvent(BaseModel):
    # For event purposes
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    timezone: str
    summary: str
    name: str
    url: str
    primary_venue: PrimaryVenue

    @property
    def tz_delta(self) -> str:
        tz = timezone(self.timezone)
        if not isinstance(tz, DstTzInfo) and not isinstance(tz, StaticTzInfo):
            return '+00:00'
        dst = tz.dst(datetime.datetime(2009, 9, 1), is_dst=True)
        if isinstance(dst, datetime.timedelta):
            return f'+0{dst.seconds//3600}:00'
        return '+00:00'

    @property
    def start(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(
            f'{self.start_date}T{self.start_time}{self.tz_delta}'
        )

    @property
    def end(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(
            f'{self.end_date}T{self.end_time}{self.tz_delta}'
        )

    def to_event(self) -> Event:
        return Event(
            name=self.name,
            description=self.summary,
            date_start=self.start,
            date_end=self.end,
            url=self.url,
            location=self.primary_venue.address.localized_address_display,
            mandatory_registration=True,
        )

    def should_record(self) -> bool:
        return True


class EventsPaginated(BaseModel):
    results: list[EBEvent]


class FullResponse(BaseModel):
    events: EventsPaginated


def parse_response(raw: str) -> list[Event]:
    data = FullResponse.model_validate_json(raw)
    return [
        event.to_event()
        for event in data.events.results
        if event.should_record()
    ]
