import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from rating_services import get_movie_details_from_tmdb, get_imdb_rating, get_rotten_tomatoes_rating

class TestRatingServices(unittest.TestCase):

    @patch('rating_services.Movie')
    def test_get_movie_details_from_tmdb_success(self, MockMovie):
        # Mock the TMDB API response for a successful lookup
        mock_movie_instance = Mock()

        # Mock for the search result
        mock_search_result = Mock()
        mock_search_result.id = 123
        mock_movie_instance.search.return_value = [mock_search_result]

        # Mock for the details result
        mock_details_result = Mock()
        mock_details_result.vote_average = 8.7
        mock_details_result.imdb_id = 'tt0133093'
        mock_movie_instance.details.return_value = mock_details_result

        MockMovie.return_value = mock_movie_instance

        # Set a dummy API key to pass the check
        with patch.dict(os.environ, {'TMDB_API_KEY': 'dummy_key'}):
            details = get_movie_details_from_tmdb("The Matrix")

        expected_details = {
            'tmdb_rating': 8.7,
            'imdb_id': 'tt0133093'
        }
        self.assertEqual(details, expected_details)

    @patch('rating_services.Movie')
    def test_get_movie_details_from_tmdb_not_found(self, MockMovie):
        # Mock the TMDB API response for a movie not found
        mock_movie_instance = Mock()
        mock_movie_instance.search.return_value = []
        MockMovie.return_value = mock_movie_instance

        with patch.dict(os.environ, {'TMDB_API_KEY': 'dummy_key'}):
            details = get_movie_details_from_tmdb("Non Existent Movie")

        self.assertIsNone(details)

    @patch('rating_services.ia')
    def test_get_imdb_rating_success(self, mock_imdb_instance):
        # Mock the IMDb API response
        mock_movie = Mock()
        mock_movie.get.return_value = 8.7

        # Configure the mock for both get_movie and update
        mock_imdb_instance.get_movie.return_value = mock_movie
        mock_imdb_instance.update.return_value = None # update doesn't return anything

        rating = get_imdb_rating("tt0133093")

        self.assertEqual(rating, 8.7)
        mock_imdb_instance.get_movie.assert_called_with('0133093')
        # Assert that update was called on the movie object
        mock_imdb_instance.update.assert_called_with(mock_movie)

    def test_get_rotten_tomatoes_rating(self):
        # Test that the function returns the "Unavailable" message
        rating = get_rotten_tomatoes_rating("Any Movie")
        self.assertEqual(rating, "Unavailable")


if __name__ == '__main__':
    unittest.main()
