import unittest
from unittest.mock import patch, Mock
import sys
import os
import requests

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from movie_lookup import get_movie_title_from_barcode

class TestMovieLookup(unittest.TestCase):

    @patch('movie_lookup.requests.get')
    def test_get_movie_title_from_barcode_success(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "title": "The Matrix"
                }
            ]
        }
        mock_get.return_value = mock_response

        # The barcode for The Matrix
        barcode = "0883929638345"
        title = get_movie_title_from_barcode(barcode)

        self.assertEqual(title, "The Matrix")

    @patch('movie_lookup.requests.get')
    def test_get_movie_title_from_barcode_not_found(self, mock_get):
        # Mock the API response for an item not found
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        barcode = "123456789012"
        title = get_movie_title_from_barcode(barcode)

        self.assertIsNone(title)

    @patch('movie_lookup.requests.get')
    def test_get_movie_title_from_barcode_api_error(self, mock_get):
        # Mock an API error
        mock_get.side_effect = requests.exceptions.RequestException("API is down")

        barcode = "0883929638345"
        title = get_movie_title_from_barcode(barcode)

        self.assertIsNone(title)

if __name__ == '__main__':
    unittest.main()
