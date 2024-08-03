import icalendar
from sqlalchemy.orm import Session

from maximus.database.schemas import DBEvent


def create_event(model: DBEvent) -> icalendar.Event:
    full_description = f'{model.description}\n\nGrattet by: {model.gratter}.'
    if model.mandatory_registration:
        full_description += '\nWarning: This event requires registration.'
    event = icalendar.Event(
        uid=str(model.id),
        summary=model.name,
        description=full_description,
        location=model.location,
        url=model.url,
        dtstart=model.date_start.date(),
        dtend=model.date_end.date(),
    )

    # Dont block time schedule in calendar
    # https://www.kanzaki.com/docs/ical/transp.html
    event.add('transp', 'TRANSPARENT')
    return event


def ics_from_db(db: Session) -> icalendar.Calendar:
    calendar = icalendar.Calendar()
    for event in db.query(DBEvent):
        calendar.add_component(create_event(event))
    return calendar
