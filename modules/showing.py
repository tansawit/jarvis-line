import requests
from bs4 import BeautifulSoup


class Movie:
    def __init__(self, name, movie_url, poster_url):
        self.name = name
        self.movie_url = movie_url
        self.poster_url = poster_url


def get_showing_list():
    base_url ='http://www.majorcineplex.com/th/main'
    page_response = requests.get(base_url)
    page_content = page_response.content
    soup = BeautifulSoup(page_content, 'html.parser')
    movie_list = list()
    for movie in soup.find_all("div", {"class": "eachMovie"}):
        name_movie = movie.select_one("div.nameMovie")

        movie_name = movie.select_one("h3.nameMovieEn").text.strip()
        movie_url = name_movie.find({'a':True}).get('href')
        poster_url=movie.find('img')

        movie = Movie(movie_name, movie_url, poster_url)
        movie_list.append(movie)
    return movie_list

def get_showing():
    movies = get_showing_list()
    for movie in movies:
        print(movies)

get_showing()