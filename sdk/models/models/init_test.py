from models import Gratters, consitent_uuid


def test_consitent_uuid() -> None:
    res = str(consitent_uuid(Gratters.MEETUP, '123456'))
    exp = 'e9b6dbc7-beae-5bd3-9f51-8a4e5e6f3c88'
    assert res == exp
