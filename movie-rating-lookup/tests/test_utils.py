import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import clean_movie_title

class TestUtils(unittest.TestCase):

    def test_clean_movie_title(self):
        # Test case based on the actual problematic title
        raw_title = "The Matrix Trilogy (4K Ultra HD + Blu-ray (Boxset)) [UHD]"
        expected_title = "The Matrix"
        self.assertEqual(clean_movie_title(raw_title), expected_title)

        # Another test case with different keywords
        raw_title = "The Lord of the Rings: The Fellowship of the Ring [DVD] (Collector's Edition)"
        expected_title = "The Lord of the Rings: The Fellowship of the Ring"
        self.assertEqual(clean_movie_title(raw_title), expected_title)

        # Test case with no changes needed
        raw_title = "Pulp Fiction"
        expected_title = "Pulp Fiction"
        self.assertEqual(clean_movie_title(raw_title), expected_title)

        # Test case with just brackets
        raw_title = "Inception [Blu-ray]"
        expected_title = "Inception"
        self.assertEqual(clean_movie_title(raw_title), expected_title)

if __name__ == '__main__':
    unittest.main()
