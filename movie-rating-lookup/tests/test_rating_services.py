import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from rating_services import get_tmdb_rating

class TestRatingServices(unittest.TestCase):

    @patch('rating_services.Movie')
    def test_get_tmdb_rating_success(self, MockMovie):
        # Mock the TMDB API response for a successful lookup
        mock_movie_instance = Mock()

        # Mock for the search result
        mock_search_result = Mock()
        mock_search_result.vote_average = 8.7
        mock_movie_instance.search.return_value = [mock_search_result]

        MockMovie.return_value = mock_movie_instance

        # Set a dummy API key to pass the check
        with patch.dict(os.environ, {'TMDB_API_KEY': 'dummy_key'}):
            rating = get_tmdb_rating("The Matrix")

        self.assertEqual(rating, 8.7)

    @patch('rating_services.Movie')
    def test_get_tmdb_rating_not_found(self, MockMovie):
        # Mock the TMDB API response for a movie not found
        mock_movie_instance = Mock()
        mock_movie_instance.search.return_value = []
        MockMovie.return_value = mock_movie_instance

        with patch.dict(os.environ, {'TMDB_API_KEY': 'dummy_key'}):
            rating = get_tmdb_rating("Non Existent Movie")

        self.assertIsNone(rating)

    def test_get_tmdb_rating_no_api_key(self):
        # Test the case where the TMDB API key is not set
        with patch.dict(os.environ, {'TMDB_API_KEY': ''}):
            rating = get_tmdb_rating("The Matrix")

        self.assertIsNone(rating)

if __name__ == '__main__':
    unittest.main()
