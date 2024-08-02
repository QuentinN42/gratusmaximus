import datetime

from gratus import Gratter
from models import Event, Gratters

gratter = Gratter.from_env(Gratters.MEETUP)
print("meetup init success")

gratter.send(
    Event(
        name='test',
        date_start=datetime.datetime.now(tz=datetime.UTC),
        date_end=datetime.datetime.now(tz=datetime.UTC),
        description="desc",
        location="desc",
        url="desc",
        mandatory_registration=False,
    )
)
print("meetup init event sent")
