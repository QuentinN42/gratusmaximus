import datetime
from textwrap import indent

from checks.checks import speak_food
from gratus import run_and_send
from meetup.gql import check, query
from meetup.parser import parse
from models import Event


def main() -> list[Event]:
    check()
    
    now = datetime.datetime.now()
    inOneWeek = now + datetime.timedelta(weeks=1)
    
    params = {"filter":{
        "lat": "48.86000061035156",
        "lon": "2.3399999141693115",
        "startDateRange": f"{now.strftime('%Y-%m-%dT%H:%M:%S')}-04:00",
        "endDateRange": f"{inOneWeek.strftime('%Y-%m-%dT%H:%M:%S')}-04:00",
        "eventType": "PHYSICAL",
    }}
    result = query('''   
          query test($filter: RecommendedEventsFilter!){
              recommendedEvents(filter: $filter){
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
    ''', params)
    
    print(result["recommendedEvents"]['pageInfo'])
    
    ret : list[Event] = []
    for d in result['recommendedEvents']['edges']:
        if (evt:=parse(d['node'])) is not None:
            if speak_food(evt.model_dump_json()):
                print(f'Event {evt.name} is accepted')
                ret.append(evt)
            else:
                print(f'Event {evt.name} is not accepted')
            
    return ret


if __name__ == "__main__":
    run_and_send(main())
