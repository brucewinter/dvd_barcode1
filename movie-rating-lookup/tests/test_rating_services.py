import unittest
from unittest.mock import patch, Mock
import sys
import os
import requests

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from rating_services import get_tmdb_rating, get_imdb_rating, get_rotten_tomatoes_rating

class TestRatingServices(unittest.TestCase):

    @patch('rating_services.Movie')
    def test_get_tmdb_rating_success(self, MockMovie):
        # Mock the TMDB API response
        mock_movie_instance = Mock()
        mock_search_result = Mock()
        mock_search_result.vote_average = 8.7
        mock_movie_instance.search.return_value = [mock_search_result]
        MockMovie.return_value = mock_movie_instance

        # Set a dummy API key to pass the check
        with patch.dict(os.environ, {'TMDB_API_KEY': 'dummy_key'}):
            rating = get_tmdb_rating("The Matrix")

        self.assertEqual(rating, 8.7)

    @patch('rating_services.ia')
    def test_get_imdb_rating_success(self, mock_imdb):
        # Mock the IMDb API response
        mock_movie = Mock()
        mock_movie.get.return_value = 8.7
        mock_imdb.search_movie.return_value = [mock_movie]

        rating = get_imdb_rating("The Matrix")

        self.assertEqual(rating, 8.7)

    @patch('rating_services.requests.get')
    def test_get_rotten_tomatoes_rating_success(self, mock_get):
        # Mock the Rotten Tomatoes page content
        mock_response = Mock()
        mock_response.status_code = 200
        # The score-board element with the tomatometerscore attribute
        mock_response.content = b'<score-board tomatometerscore="87"></score-board>'
        mock_get.return_value = mock_response

        rating = get_rotten_tomatoes_rating("The Matrix")

        self.assertEqual(rating, "87%")

    @patch('rating_services.requests.get')
    def test_get_rotten_tomatoes_rating_not_found(self, mock_get):
        # Mock a 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        rating = get_rotten_tomatoes_rating("Non Existent Movie")

        self.assertIsNone(rating)


if __name__ == '__main__':
    unittest.main()
