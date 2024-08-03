from eventbrite.parser import parse_response
from eventbrite.scrapper import get_data

print("Eventbrite scrapping started!")


print(parse_response(get_data()))
