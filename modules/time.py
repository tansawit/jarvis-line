import os
from datetime import datetime
from os.path import join, dirname
from pathlib import Path

import requests
from dotenv import load_dotenv

dotenv_path = join(str(Path(dirname(__file__), '.env').parent.parent), '.env')
print("====PATH=====")
print(dotenv_path)
load_dotenv(dotenv_path)

MAPQUEST_CONSUMER_KEY = str(os.environ.get("MAPQUEST_CONSUMER_KEY"))
TIME_ZONE_DB_API_KEY = str(os.environ.get("TIME_ZONE_DB_API_KEY"))


def get_time(location):
    print(location)
    try:
        mapquest_url = 'http://open.mapquestapi.com/nominatim/v1/search.php?key=' + MAPQUEST_CONSUMER_KEY + '&format=json&q=' + location + '&limit=1'
        r = requests.get(mapquest_url)
        location_data = r.json()
        r = requests.get('http://api.timezonedb.com/?lat=' + location_data[0]['lat'] + '&lng=' + location_data[0][
            'lon'] + '&format=json&key=' + TIME_ZONE_DB_API_KEY)
        time_data = r.json()
        time = datetime.utcfromtimestamp(time_data['timestamp']).strftime('%a %b %d %Y %H:%M:%S')
        print(time)
        output = 'Location: ' + location_data[0]['display_name'] + '\nTime: ' + time + ' ' + time_data[
            'abbreviation']

    except:
        error_message = 'I couldn\'t get the time at the location you specified.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - time in new york'
        error_message += '\n  - india time'
        error_message += '\n  - time at paris'
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
