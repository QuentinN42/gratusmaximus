import json

import httpx

RAW_REQUEST = {
    "event_search": {
        "dates": "current_future",
        "dedup": True,
        "places": ["101751119"],
        "price": "free",
        "tags": ["EventbriteCategory/101"],
        "page": 1,
        "page_size": 20,
        "online_events_only": False,
        "languages": ["fr"],
    },
    "expand.destination_event": [
        "primary_venue",
        "image",
        "ticket_availability",
        "saves",
        "event_sales_status",
        "primary_organizer",
        "public_collections",
    ],
    "browse_surface": "search",
}
TARGET_URL = 'https://www.eventbrite.com/api/v3/destination/search/'


def get_data() -> str:
    csrf_resp = httpx.get(
        'https://www.eventbrite.com/d/france--paris/free--business--events/'
    )
    csrf_resp.raise_for_status()
    csrf = csrf_resp.cookies.get('csrftoken') or ''
    if not csrf:
        raise Exception('No CSRF token found')
    resp = httpx.post(
        TARGET_URL,
        headers={
            'Referer': TARGET_URL,
            'Cookie': f'csrftoken={csrf}',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        content=json.dumps(RAW_REQUEST),
    )
    resp.raise_for_status()

    return resp.content.decode('utf-8')
