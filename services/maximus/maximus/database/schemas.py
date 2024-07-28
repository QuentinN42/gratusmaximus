import logging
import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """declarative base class"""


metadata = Base.metadata


class Events(Base):
    __tablename__ = 'events'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
