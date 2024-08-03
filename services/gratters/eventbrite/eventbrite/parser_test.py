import datetime

import pytest

from eventbrite.parser import Address, EBEvent, PrimaryVenue


def evt(
    start_date: str = '',
    start_time: str = '',
    timezone: str = '',
) -> EBEvent:
    return EBEvent(
        start_date=start_date,
        start_time=start_time,
        timezone=timezone,
        end_date='',
        end_time='',
        summary='',
        name='',
        url='',
        primary_venue=PrimaryVenue(
            address=Address(localized_address_display='')
        ),
    )


@pytest.mark.parametrize(
    ('timezone', 'expected'),
    [
        ("Europe/Paris", '+01:00'),
        ("CET", '+01:00'),
        ("GMT", '+00:00'),
        ("Europe/London", '+01:00'),
    ],
)
def test_tz_delta(
    timezone: str,
    expected: str,
) -> None:
    assert evt(timezone=timezone).tz_delta == expected


@pytest.mark.parametrize(
    (
        "start_date",
        "start_time",
        "timezone",
        "expected",
    ),
    [
        (
            "2024-09-05",
            "10:30",
            "Europe/Paris",
            datetime.datetime(
                2024,
                9,
                5,
                10,
                30,
                tzinfo=datetime.timezone(datetime.timedelta(hours=1)),
            ),
        )
    ],
)
def test_date_parsed(
    start_date: str,
    start_time: str,
    timezone: str,
    expected: datetime.datetime,
) -> None:
    date = evt(
        start_date=start_date,
        start_time=start_time,
        timezone=timezone,
    ).start
    assert isinstance(date, datetime.datetime)
    assert date.tzinfo is not None
    assert date == expected
