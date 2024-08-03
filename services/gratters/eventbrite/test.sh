#!/bin/bash

## CSRF Token
curl -v -o /dev/null https://www.eventbrite.com/d/france--paris/free--business--events/ 2>&1 | grep 'csrftoken='

## Search
curl 'https://www.eventbrite.com/api/v3/destination/search/' \
    -X POST \
    -H 'Referer: https://www.eventbrite.com/d/france--paris/free--business--events/?page=1&lang=fr' \
    -H 'Cookie: csrftoken=107c825e504c11ef9f092b9c04571f72' \
    -H 'Accept: */*' \
    -H 'Content-Type: application/json' \
    -H 'X-CSRFToken: 107c825e504c11ef9f092b9c04571f72' \
    --data-raw '{"event_search":{"dates":"current_future","dedup":true,"places":["101751119"],"price":"free","tags":["EventbriteCategory/101"],"page":1,"page_size":20,"online_events_only":false,"languages":["fr"]},"expand.destination_event":["primary_venue","image","ticket_availability","saves","event_sales_status","primary_organizer","public_collections"],"browse_surface":"search"}' \
    | jq
