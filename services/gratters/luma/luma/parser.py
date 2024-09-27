import datetime
from typing import Any

from models import Event, Gratters, consitent_uuid

from luma.types import LumaEvent


def parse(data: str) -> Event:
    evt = LumaEvent.model_validate_json(data)
    location = evt.event.geo_address_info.full_address
    if not location:
        location = evt.event.geo_latitude + ' ' + evt.event.geo_longitude
    return Event(
        id=consitent_uuid(Gratters.LUMA, evt.api_id),
        name=evt.event.name,
        date_start=datetime.datetime.fromisoformat(evt.event.start_at),
        date_end=datetime.datetime.fromisoformat(evt.event.end_at),
        description=_r_rebuild_desc(evt.description_mirror).strip(),
        location=location,
        url=f'https://lu.ma/{evt.event.url}',
        mandatory_registration=True,
    )


def _r_rebuild_desc(data: dict[str, Any]) -> str:
    res = data.get('text', '')

    if data.get('content'):
        if isinstance(data['content'], list):
            for item in data['content']:
                if isinstance(item, dict):
                    res += _r_rebuild_desc(item)
                else:
                    print(f'WARN: item is not a dict : {item}')
        else:
            print(f'WARN: content is not a list : {data["content"]}')

    if data.get('type') == 'hard_break':
        res += '\n'
    elif data.get('type') == 'paragraph':
        res += '\n\n'

    return res
