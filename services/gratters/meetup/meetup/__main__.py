import datetime

from gratus import Gratter
from models import Event, Gratters

gratter = Gratter.from_env(Gratters.MEETUP)
print("meetup init success")

gratter.send(
    Event(
        name='test with other tz',
        date_start=datetime.datetime.now(
            tz=datetime.timezone(datetime.timedelta(hours=10))
        )
        + datetime.timedelta(hours=1),
        date_end=datetime.datetime.now(
            tz=datetime.timezone(datetime.timedelta(hours=10))
        )
        + datetime.timedelta(hours=1),
        description="desc",
        location="desc",
        url="desc",
        mandatory_registration=False,
    )
)
print("meetup init event sent")
