import datetime
from typing import Generator

from services.meetup.gql import query

raw_query = '''   
query test($filter: RecommendedEventsFilter!, $after: String) {
    recommendedEvents(filter: $filter, after: $after) {
        pageInfo {
            hasNextPage
            endCursor
        }
        edges {
            node {
                id
                title
                description
                eventUrl
                venue {
                    name
                    address
                    city
                    eventVenueOptions {
                        feeSettings {
                            amount
                        }
                    }
                }
                dateTime
                endTime
            }
        }
    }
}
'''


def collect() -> Generator[dict, None, None]:
    now = datetime.datetime.now()
    inOneWeek = now + datetime.timedelta(weeks=1)
    hasNext = True
    after = None

    while hasNext:
        params = {
            "filter": {
                "lat": "48.86000061035156",
                "lon": "2.3399999141693115",
                "startDateRange": f"{now.strftime('%Y-%m-%dT%H:%M:%S')}-04:00",
                "endDateRange": f"{inOneWeek.strftime('%Y-%m-%dT%H:%M:%S')}-04:00",
                "eventType": "PHYSICAL",
            },
            "after": after,
        }
        result = query(raw_query, params)

        print(result["recommendedEvents"]['pageInfo'])

        hasNext = result["recommendedEvents"]['pageInfo']['hasNextPage']
        after = result["recommendedEvents"]['pageInfo']['endCursor']

        for d in result['recommendedEvents']['edges']:
            yield d['node']
