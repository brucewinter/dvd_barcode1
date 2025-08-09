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

def get_movie_details_from_tmdb(movie_title):
    """
    Gets movie details (TMDB rating and IMDb ID) from The Movie Database.

    Args:
        movie_title (str): The title of the movie to look up.

    Returns:
        dict: A dictionary with 'tmdb_rating' and 'imdb_id', or None.
    """
    if not tmdb.api_key:
        return None
    try:
        movie = Movie()
        search = movie.search(movie_title)

        first_result = next(iter(search), None)

        if first_result:
            details = movie.details(first_result.id)
            return {
                'tmdb_rating': details.vote_average,
                'imdb_id': details.imdb_id
            }
    except TMDbException as e:
        print(f"Error fetching from TMDb: {e}")
    return None

def get_imdb_rating(imdb_id):
    """
    Gets the rating for a movie from IMDb using its IMDb ID.

    Args:
        imdb_id (str): The IMDb ID of the movie (e.g., 'tt0133093').

    Returns:
        float: The IMDb rating, or None if not found.
    """
    if not imdb_id:
        return None
    try:
        # IMDb IDs are passed without the 'tt' prefix to get_movie
        movie_id_digits = imdb_id.replace('tt', '')
        movie = ia.get_movie(movie_id_digits)
        if movie:
            return movie.get('rating')
    except IMDbError as e:
        print(f"Error fetching from IMDb: {e}")
    return None

def get_rotten_tomatoes_rating(movie_title):
    """
    Gets the rating for a movie from Rotten Tomatoes.
    NOTE: This feature is currently disabled due to website scraping blocks.
    """
    # print("Rotten Tomatoes lookup is currently unavailable.")
    return "Unavailable"
