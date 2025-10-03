import httpx


def get_events_ids() -> list[str]:
    print('Fetching events ids ...')
    alls = httpx.get('https://api.lu.ma/url?url=paris')
    alls.raise_for_status()
    print('Fetched events ids')
    data1 = alls.json()
    assert isinstance(data1, dict), f"data1 is not a dict: {data1}"
    data1_data = data1.get('data', {})
    assert isinstance(
        data1_data, dict
    ), f"data1_data is not a dict: {data1_data}"
    data1_data_events = data1_data.get('events', [])
    assert isinstance(
        data1_data_events, list
    ), f"data1_data_events is not a list: {data1_data_events}"

    print(f'Found {len(data1_data_events)} events ids')
    ids: list[str] = []
    for item in data1_data_events:
        if not isinstance(item, dict):
            print(f'WARN: item is not a dict : {item}')
            continue
        event = item.get('event', {})
        if not isinstance(event, dict):
            print(f'WARN: event is not a dict : {event}')
            continue
        api_id = event.get('api_id')
        if not isinstance(api_id, str):
            print(f'WARN: api_id is not a str : {api_id}')
            continue
        ids.append(api_id)
    print(f'All events ids processed : {len(ids)} to process')
    return ids
