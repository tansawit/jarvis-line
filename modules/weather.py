import requests

def get_weather(location):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"units": "metric", "q": location}
    
    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "2ab9952035mshaf99810b4e29671p12d6e8jsn26097042d4a5"
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.json())
        weather_response = response.json()
        output = f"Weather in {weather_response['name']}:"
        output += f"\nCurrent Condition: {weather_response['weather'][0]['main']}-{weather_response['weather'][0]['description']}"
        output += f"\nCurrent Temperature: {weather_response['main']['temp']} °C"
        output += f"\nHigh: {weather_response['main']['temp_max']} °C"
        output += f"\nMin: {weather_response['main']['temp_min']} °C"
    except:
        error_message = 'I couldn\'t get the weather info you asked for.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - tell me the weather in London'
        error_message += '\n  - weather Delhi'
        error_message += '\n  - What\'s the weather in Texas?'
        output = error_message
    output = {"fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        output
                    ]
                }
            }
        ],
        }
    return output


