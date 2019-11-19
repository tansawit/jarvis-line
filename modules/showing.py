import sqlite3
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def update_showing_list():
    conn = sqlite3.connect("showing.db")
    c = conn.cursor()
    current_datetime = datetime.now()

    last_checked_cursor = c.execute("SELECT lastChecked FROM showingStats ORDER BY ROWID ASC LIMIT 1").fetchone()
    last_checked_datetime = datetime.strptime(last_checked_cursor[0], "%d/%m/%Y %H:%M:%S")

    time_since_last_update = current_datetime - last_checked_datetime
    if time_since_last_update.seconds > (60 * 60 * 12):
        print("Fetching New Movies")
        base_url = 'http://www.majorcineplex.com/th/main'
        page_response = requests.get(base_url)
        page_content = page_response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        for movie in soup.find_all("div", {"class": "eachMovie"}):
            name_movie = movie.select_one("div.nameMovie")

            movie_name = movie.select_one("h3.nameMovieEn").text.strip()
            movie_url = name_movie.find({'a': True}).get('href')
            poster_url = movie.find('img')['src']
            release_date = movie.select_one("p.releaseDate").text.strip()
            movie_desc = movie.select_one("div.explain").select_one("div.thirdexplain").select_one(
                "span.overflow").select_one("p").select_one("p").text.strip()

            c.execute("INSERT OR IGNORE INTO showing (name,movieUrl,posterUrl,releaseDate,desc) VALUES (?,?,?,?,?)",
                      (movie_name, movie_url, poster_url, release_date[15:], movie_desc))
            conn.commit()
    else:
        print("Using Stored List")


def get_showing():
    update_showing_list()
    conn = sqlite3.connect("showing.db")
    movies_cursor = conn.execute("SELECT * FROM showing")
    desc = movies_cursor.description
    column_names = [col[0] for col in desc]
    movies = [dict(zip(column_names, row)) for row in movies_cursor]
    showing_list = list()
    for movie in movies[:10]:
        showing_list.append(
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": f"{movie['posterUrl']}",
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
                            "text": f"{movie['name']}",
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
                                    "text": f"Release Date:"
                                            f" {datetime.strptime(movie['releaseDate'], '%d/%m/%y').strftime('%d %B %Y')}",
                                    "style": "normal",
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
                                "label": "Website",
                                "uri": f"{movie['movieUrl']}"
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
        )
    res = {
        "fulfillmentMessages": [
            {
                "payload": {
                    "line": {
                        "altText": "Message",
                        "type": "flex",
                        "contents": {
                            "type": "carousel",
                            "contents": showing_list
                        }
                    }
                },
            }
        ]
    }
    return res


get_showing()
