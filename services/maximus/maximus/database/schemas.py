import datetime
import logging
import uuid

from models import Event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """declarative base class"""


metadata = Base.metadata


def date_to_utc(date: datetime.datetime) -> datetime.datetime:
    if date.tzinfo is None:
        logger.warning("No timezone info provided, assuming UTC")
        return date.replace(tzinfo=datetime.timezone.utc)

    return date.astimezone(datetime.timezone.utc).replace(tzinfo=None)


class DBEvent(Base):
    __tablename__ = 'events'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    date_start: Mapped[datetime.datetime] = mapped_column()
    date_end: Mapped[datetime.datetime] = mapped_column()
    description: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    mandatory_registration: Mapped[bool] = mapped_column()

    gratter: Mapped[str] = mapped_column()

    @classmethod
    def from_model(cls, event: Event) -> 'DBEvent':
        return cls(
            id=uuid.uuid4(),
            name=event.name,
            date_start=date_to_utc(event.date_start),
            date_end=date_to_utc(event.date_end),
            description=event.description,
            location=event.location,
            url=event.url,
            mandatory_registration=event.mandatory_registration,
        )


class DBKeys(Base):
    __tablename__ = 'keys'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default='')
