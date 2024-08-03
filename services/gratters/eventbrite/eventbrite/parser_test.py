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


@pytest.mark.parametrize(
    ('event', 'ok'),
    [
        (
            EBEvent(
                start_date='2024-09-19',
                start_time='09:00',
                end_date='2024-09-21',
                end_time='17:00',
                timezone='Europe/Paris',
                summary='Le leadership au féminin  va transformer le monde des affaires et prenant soin des besoins de toutes les parties prenantes',
                name='LEADERSHIP AU FÉMININ',
                url='https://www.eventbrite.fr/e/billets-leadership-au-feminin-55543912337',
                primary_venue=PrimaryVenue(
                    address=Address(localized_address_display='Paris, Paris')
                ),
            ),
            False,
        ),
        (
            EBEvent(
                start_date='2024-09-05',
                start_time='08:45',
                end_date='2024-09-05',
                end_time='10:30',
                timezone='Europe/Paris',
                summary='Emilie et Mathieu, experts en direction commerciale externalisée vont vous donner des tips ultra concrets pour composer votre routine newbiz',
                name="Petit-déjeuner L'ADN Data: Le New Business : de la vision à l'action",
                url='https://www.eventbrite.fr/e/billets-petit-dejeuner-ladn-data-le-new-business-de-la-vision-a-laction-945518891457',
                primary_venue=PrimaryVenue(
                    address=Address(
                        localized_address_display='13 Rue Chapon, 75003 Paris'
                    )
                ),
            ),
            True,
        ),
    ],
)
def test_should_record(event: EBEvent, ok: bool) -> None:
    assert event.should_record() is ok
