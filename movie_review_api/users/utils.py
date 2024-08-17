import requests
import os
from time import sleep
from .models import Genre


def fetch_movie_data(movie_id):
    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise ValueError("TMDB_API_KEY environment variable is not set")

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie data: {e}")
        raise


def fetch_movies(page=1, retries=3):
    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise ValueError("TMDB_API_KEY environment variable is not set")

    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error fetching movies (attempt {attempt + 1}/{retries}): {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request Error fetching movies (attempt {attempt + 1}/{retries}): {e}")
        if attempt < retries - 1:
            sleep(5)  # Wait before retrying
        else:
            raise

    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise ValueError("TMDB_API_KEY environment variable is not set")

    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movies (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                sleep(5)  # Wait before retrying
            else:
                raise


def fetch_all_movies(max_count=30):
    page = 1
    all_movies = []
    while len(all_movies) < max_count:
        print(f"Fetching page {page}")  # Logging
        data = fetch_movies(page)
        movies = data.get('results', [])

        if not movies:
            break  # Exit loop if no more movies are returned

        all_movies.extend(movies)
        page += 1

        # Check if we have reached the last page
        if data.get('page', 1) >= data.get('total_pages', 1):
            break

    # Truncate the list to the max_count if we fetched more movies
    return all_movies[:max_count]





def fetch_genres():
    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise ValueError("TMDB_API_KEY environment variable is not set")

    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('genres', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching genres: {e}")
        raise


def save_genres():
    genres = fetch_genres()
    for genre_data in genres:
        genre, created = Genre.objects.get_or_create(tmdb_id=genre_data['id'], defaults={'name': genre_data['name']})
        if not created:
            genre.name = genre_data['name']
            genre.save()
