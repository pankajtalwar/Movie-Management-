import requests

class MovieClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3'

    def get_movie_details(self, movie_id):
        url = f"{self.base_url}/movie/{movie_id}?api_key={self.api_key}"
        response = requests.get(url)
        return response.json()

    def search_movies(self, query):
        url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={query}"
        response = requests.get(url)
        return response.json()
