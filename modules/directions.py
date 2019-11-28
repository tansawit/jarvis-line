import os
from os.path import join, dirname
from pathlib import Path

import requests

GOOGLE_MAPS_API_KEY = str(os.environ.get("GOOGLE_MAPS_API_KEY"))


def get_directions(location):
    try:
        maps_query_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' \
                         + location \
                         + '&inputtype=textquery&fields=photos,formatted_address,name,opening_hours,geometry&key=' \
                         + GOOGLE_MAPS_API_KEY
        r = requests.get(maps_query_url).json()
        print("===RESPONSE===")
        print(r)
        print("===RESPONSE===")
        location_name = r['candidates'][0]['name']
        location_hours = "Open Now" if r['candidates'][0]['opening_hours']['open_now'] else "Closed"
        location_address = r['candidates'][0]['formatted_address']
        location_lat_long = [r['candidates'][0]['geometry']['location']['lat'],
                             r['candidates'][0]['geometry']['location']['lng']]
        print(location_hours)
        output = {"fulfillmentMessages": [
            {
                "payload": {
                    "line": {
                        "type": "location",
                        "address": location_address,
                        "title": location_name,
                        "latitude": location_lat_long[0],
                        "longitude": location_lat_long[1]
                    }
                },
                "platform": "LINE"
            },
            {
                "text": {
                    "text": [
                        ""
                    ]
                }
            }
        ],
        }
    except:
        error_message = 'I couldn\'t get the the location you specified.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - direction to Siam Paragon'
        error_message += '\n  - how to get to Central World'
        output = error_message
        output = {"fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        output
                    ]
                }
            },
        ],
        }
    return output
