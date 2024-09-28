import typing

import httpx


def query(txt: str) -> dict[str, typing.Any]:
    res = httpx.post('https://www.meetup.com/gql2', json={'query': txt})
    res.raise_for_status()

    resp = res.json()
    assert isinstance(resp, dict), f'Got HTTP response: {resp}'

    if errs := resp.get('errors'):
        if isinstance(errs, list):
            for err in errs:
                print(f'Got GQL ERROR: {err}')
        else:
            print(f'Got GQL ERRORS: {resp["errors"]}')

    data = resp.get('data') or {}
    assert isinstance(data, dict), f'Got invalid GQL DATA: {data}'
    return data


def check() -> None:
    if query('query { __typename }') == {'__typename': 'Query'}:
        print('Able to query Meetup GQL')
    else:
        print('Unable to query Meetup GQL')
        raise SystemExit(1)
