import os
from tmdbv3api import TMDb, Movie
from tmdbv3api.exceptions import TMDbException

# Initialize TMDB
tmdb = TMDb()
# It's recommended to set the API key as an environment variable
tmdb.api_key = os.environ.get('TMDB_API_KEY')
if not tmdb.api_key:
    print("Warning: TMDB_API_KEY environment variable not set. TMDB lookups will fail.")
    print("Get a key from https://www.themoviedb.org/documentation/api and set it as an environment variable.")

def get_tmdb_rating(movie_title):
    """
    Gets a movie's rating from The Movie Database (TMDb).

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

        first_result = next(iter(search), None)

        if first_result:
            # The search result object itself contains the vote_average
            return first_result.vote_average
    except TMDbException as e:
        print(f"Error fetching from TMDb: {e}")
    return None
