import datetime

from gratus import Gratter
from models import Event, Gratters

gratter = Gratter.from_env(Gratters.MEETUP)
print("meetup init success")

gratter.send(
    Event(
        name='test',
        date_start=datetime.datetime.now(tz=datetime.UTC)
        + datetime.timedelta(hours=1),
        date_end=datetime.datetime.now(tz=datetime.UTC)
        + datetime.timedelta(hours=3),
        description="desc",
        location="desc",
        url="desc",
        mandatory_registration=False,
    )
)
print("meetup init event sent")
