import datetime
import uuid

import pytest

from sdk.models import Event
from services.maximus.database.schemas import DBEvent, date_to_utc


def dt(hour: int, tz_delta: int) -> datetime.datetime:
    return datetime.datetime(
        2021,
        1,
        1,
        hour,
        0,
        0,
        tzinfo=datetime.timezone(datetime.timedelta(hours=tz_delta)),
    )


DT_TESTS: dict[datetime.datetime, datetime.datetime] = {
    dt(10, tz_delta=0): dt(10, tz_delta=0),
    dt(10, tz_delta=-1): dt(11, tz_delta=0),
    dt(10, tz_delta=1): dt(9, tz_delta=0),
}


@pytest.mark.parametrize(
    ("provided", "expected"),
    list(DT_TESTS.items()),
)
def test_date_to_utc(
    provided: datetime.datetime,
    expected: datetime.datetime,
):
    res = date_to_utc(provided)
    assert res.tzinfo in [datetime.timezone.utc, None]
    assert res.hour == expected.hour


@pytest.mark.parametrize(
    ("provided", "expected"),
    list(DT_TESTS.items()),
)
def test_datetime_parsed_to_utc(
    provided: datetime.datetime,
    expected: datetime.datetime,
):
    event = Event(
        id=uuid.UUID(int=42),
        date_start=provided,
        date_end=provided,
        name="",
        description="",
        location="",
        url="",
        mandatory_registration=False,
    )
    db_event = DBEvent.from_model(event)

    # assert no tzinfo
    assert db_event.date_start.tzinfo in [datetime.timezone.utc, None]
    assert db_event.date_end.tzinfo in [datetime.timezone.utc, None]

    assert db_event.date_start.hour == expected.hour
    assert db_event.date_end.hour == expected.hour
