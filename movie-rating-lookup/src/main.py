import argparse
from movie_lookup import get_movie_title_from_barcode
from rating_services import get_tmdb_rating
from utils import clean_movie_title

def main():
    """
    Main function to get a movie rating from a barcode.
    """
    parser = argparse.ArgumentParser(description="Look up a movie rating from a barcode.")
    parser.add_argument("barcode", help="The UPC barcode of the DVD.")
    args = parser.parse_args()

    print(f"Looking up movie for barcode: {args.barcode}")
    raw_movie_title = get_movie_title_from_barcode(args.barcode)

    if not raw_movie_title:
        print("Could not find a movie for this barcode.")
        return

    print(f"Found movie title: {raw_movie_title}")

    # Clean the title to improve search results
    cleaned_title = clean_movie_title(raw_movie_title)
    print(f"Cleaned title for searching: {cleaned_title}")
    print("-" * 20)

    print("Fetching rating from TMDB...")

    tmdb_rating = get_tmdb_rating(cleaned_title)

    print("\n--- Rating ---")
    if tmdb_rating:
        print(f"TMDb Rating: {tmdb_rating} / 10")
    else:
        print("TMDb Rating: Not found")
    print("--------------")

if __name__ == "__main__":
    main()
