import httpx

from sdk.models import Event
from services.luma.parser import parse


def fetch_one(_id: str) -> Event:
    print(f'Fetching {_id} ...')
    res = httpx.get('https://api.lu.ma/event/get', params={"event_api_id": _id})
    res.raise_for_status()
    print(f'Fetched {_id}')
    print(f'Parsing {_id} ...')
    parsed = parse(res.text)
    print(f'Parsed {_id}')
    return parsed
