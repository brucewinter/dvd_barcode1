import os
import requests
from bs4 import BeautifulSoup
from tmdbv3api import TMDb, Movie
from tmdbv3api.exceptions import TMDbException
from imdb import IMDb, IMDbError

# Initialize TMDB
tmdb = TMDb()
# It's recommended to set the API key as an environment variable
tmdb.api_key = os.environ.get('TMDB_API_KEY')
if not tmdb.api_key:
    print("Warning: TMDB_API_KEY environment variable not set. TMDB lookups will fail.")
    print("Get a key from https://www.themoviedb.org/documentation/api and set it as an environment variable.")


# Initialize IMDb
ia = IMDb()

def get_tmdb_rating(movie_title):
    """
    Gets the rating for a movie from The Movie Database (TMDb).

    Args:
        movie_title (str): The title of the movie to look up.

    Returns:
        float: The TMDb rating, or None if not found.
    """
    if not tmdb.api_key:
        return None
    try:
        movie = Movie()
        search = movie.search(movie_title)
        if search:
            result = search[0]
            return result.vote_average
    except TMDbException as e:
        print(f"Error fetching from TMDb: {e}")
    return None

def get_imdb_rating(movie_title):
    """
    Gets the rating for a movie from IMDb.

    Args:
        movie_title (str): The title of the movie to look up.

    Returns:
        float: The IMDb rating, or None if not found.
    """
    try:
        movies = ia.search_movie(movie_title)
        if movies:
            movie = movies[0]
            ia.update(movie)
            return movie.get('rating')
    except IMDbError as e:
        print(f"Error fetching from IMDb: {e}")
    return None

def get_rotten_tomatoes_rating(movie_title):
    """
    Gets the rating for a movie from Rotten Tomatoes by scraping.

    Args:
        movie_title (str): The title of the movie to look up.

    Returns:
        str: The Rotten Tomatoes rating (e.g., "95%"), or None if not found.
    """
    try:
        # Format movie title for URL, removing special characters
        formatted_title = ''.join(c for c in movie_title if c.isalnum() or c.isspace()).lower().replace(' ', '_')
        url = f"https://www.rottentomatoes.com/m/{formatted_title}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        score_element = soup.find('score-board')
        if score_element and score_element.attrs.get('tomatometerscore'):
            return score_element.attrs.get('tomatometerscore') + '%'

    except requests.exceptions.RequestException as e:
        # It's common for this to fail if the movie title doesn't map perfectly to a URL
        # So we don't print an error unless it's a non-404 error.
        if e.response and e.response.status_code != 404:
             print(f"Error fetching Rotten Tomatoes page for '{movie_title}': {e}")

    return None
