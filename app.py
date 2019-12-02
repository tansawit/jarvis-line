import json
import os

from flask import Flask, make_response, request

from modules import (
    weather,
    time,
    directions,
    showing
)

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)
    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    intent = req_dict["queryResult"]["intent"]["displayName"]
    print(f"INTENT = {intent}")
    if intent == 'weather':
        weather_location = str()
        if req_dict["queryResult"]["parameters"]["geo-city"]:
            weather_location = req_dict["queryResult"]["parameters"]["geo-city"]
        else:
            weather_location = req_dict["queryResult"]["parameters"]["geo-country"]
        res = weather.get_weather(weather_location)
    elif intent == 'world-clock':
        if req_dict["queryResult"]["parameters"]["geo-city"]:
            clock_location = req_dict["queryResult"]["parameters"]["geo-city"]
        else:
            clock_location = req_dict["queryResult"]["parameters"]["geo-country"]
        res = time.get_time(clock_location)

    # Knowledge Base
    elif "Knowledge.KnowledgeBase" in intent:
        res = {"fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        req_dict['queryResult']['fulfillmentText']
                    ]
                }
            },
        ],
        }

    # Personal Files/Links
    elif intent == 'resume':
        res = {"fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"https://tansawit.me/sawit-trisirisatayawong-resume.pdf"
                    ]
                }
            },
        ],
        }
    elif intent == 'linkedin':
        res = {"fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"https://www.linkedin.com/in/tansawit/"
                    ]
                }
            },
        ],
        }
    elif intent == 'instagram':
        res = {"fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"https://www.instagram.com/tansawit/",
                    ],
                },
            },
            {
                "text": {
                    "text": [
                        f"https://www.instagram.com/sawittan/"
                    ],
                }
            }
        ],
        }

    # TEST
    elif intent == 'directions':
        directions_type, directions_location = \
            next((k, v) for k, v in req_dict["queryResult"]
                 ["parameters"]["location"].items() if v)
        res = directions.get_directions(
            directions_location.replace(' ', '%20'))
    elif intent == 'showing':
        res = showing.get_showing()
    elif intent == 'test':
        res = {
            "fulfillmentMessages": [
                {
                    "payload": {
                        "line": {
                            "altText": "Message",
                            "type": "flex",
                            "contents": {
                                "type": "carousel",
                                "contents": [
                                    {
                                        "type": "bubble",
                                        "hero": {
                                            "type": "image",
                                            "url": "https://cdn.majorcineplex.com/uploads/movie/2601/thumb_2601.jpg?1571964618",
                                            "size": "full",
                                            "aspectMode": "cover",
                                            "action": {
                                                "type": "uri",
                                                "uri": "http://linecorp.com/"
                                            },
                                            "aspectRatio": "3:4",
                                            "gravity": "bottom"
                                        },
                                        "body": {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "Frozen 2",
                                                    "weight": "bold",
                                                    "size": "xl"
                                                },
                                                {
                                                    "type": "box",
                                                    "layout": "vertical",
                                                    "margin": "lg",
                                                    "spacing": "sm",
                                                    "contents": [
                                                        {
                                                            "type": "text",
                                                            "text": "วันที่เข้าฉาย: 21/11/19",
                                                            "style": "normal",
                                                            "weight": "bold"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        "footer": {
                                            "type": "box",
                                            "layout": "vertical",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "button",
                                                    "style": "link",
                                                    "height": "sm",
                                                    "action": {
                                                        "type": "postback",
                                                        "label": "Description",
                                                        "data": "Frozen"
                                                    }
                                                },
                                                {
                                                    "type": "button",
                                                    "style": "link",
                                                    "height": "sm",
                                                    "action": {
                                                        "type": "uri",
                                                        "label": "WEBSITE",
                                                        "uri": "https://linecorp.com"
                                                    }
                                                },
                                                {
                                                    "type": "spacer",
                                                    "size": "sm"
                                                }
                                            ],
                                            "flex": 0
                                        }
                                    },
                                    {
                                        "footer": {
                                            "type": "box",
                                            "layout": "vertical",
                                            "spacing": "sm",
                                            "flex": 0,
                                            "contents": [
                                                {
                                                    "style": "link",
                                                    "height": "sm",
                                                    "action": {
                                                        "type": "uri",
                                                        "uri": "https://linecorp.com",
                                                        "label": "CALL"
                                                    },
                                                    "type": "button"
                                                },
                                                {
                                                    "style": "link",
                                                    "height": "sm",
                                                    "action": {
                                                        "type": "uri",
                                                        "uri": "https://linecorp.com",
                                                        "label": "WEBSITE"
                                                    },
                                                    "type": "button"
                                                },
                                                {
                                                    "type": "spacer",
                                                    "size": "sm"
                                                }
                                            ]
                                        },
                                        "hero": {
                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                                            "action": {
                                                "type": "uri",
                                                "uri": "http://linecorp.com/"
                                            },
                                            "type": "image",
                                            "aspectRatio": "20:13",
                                            "size": "full",
                                            "aspectMode": "cover"
                                        },
                                        "body": {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "Brown Cafe",
                                                    "weight": "bold",
                                                    "size": "xl"
                                                },
                                                {
                                                    "margin": "md",
                                                    "type": "box",
                                                    "layout": "baseline",
                                                    "contents": [
                                                        {
                                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                                            "size": "sm",
                                                            "type": "icon"
                                                        },
                                                        {
                                                            "type": "icon",
                                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                                            "size": "sm"
                                                        },
                                                        {
                                                            "type": "icon",
                                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                                            "size": "sm"
                                                        },
                                                        {
                                                            "type": "icon",
                                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                                            "size": "sm"
                                                        },
                                                        {
                                                            "type": "icon",
                                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
                                                            "size": "sm"
                                                        },
                                                        {
                                                            "text": "4.0",
                                                            "type": "text",
                                                            "size": "sm",
                                                            "color": "#999999",
                                                            "margin": "md",
                                                            "flex": 0
                                                        }
                                                    ]
                                                },
                                                {
                                                    "margin": "lg",
                                                    "type": "box",
                                                    "layout": "vertical",
                                                    "spacing": "sm",
                                                    "contents": [
                                                        {
                                                            "type": "box",
                                                            "layout": "baseline",
                                                            "spacing": "sm",
                                                            "contents": [
                                                                {
                                                                    "flex": 1,
                                                                    "size": "sm",
                                                                    "color": "#aaaaaa",
                                                                    "type": "text",
                                                                    "text": "Place"
                                                                },
                                                                {
                                                                    "type": "text",
                                                                    "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                                                                    "size": "sm",
                                                                    "color": "#666666",
                                                                    "flex": 5,
                                                                    "wrap": True
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "contents": [
                                                                {
                                                                    "size": "sm",
                                                                    "color": "#aaaaaa",
                                                                    "type": "text",
                                                                    "text": "Time",
                                                                    "flex": 1
                                                                },
                                                                {
                                                                    "type": "text",
                                                                    "text": "10:00 - 23:00",
                                                                    "size": "sm",
                                                                    "color": "#666666",
                                                                    "flex": 5,
                                                                    "wrap": True
                                                                }
                                                            ],
                                                            "type": "box",
                                                            "layout": "baseline",
                                                            "spacing": "sm"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        "type": "bubble"
                                    }
                                ]
                            }
                        }
                    },
                }
            ]
        }
    return res


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
