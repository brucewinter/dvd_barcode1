import argparse
from movie_lookup import get_movie_title_from_barcode
from rating_services import get_movie_details_from_tmdb, get_imdb_rating, get_rotten_tomatoes_rating
from utils import clean_movie_title

def main():
    """
    Main function to get movie ratings from a barcode.
    """
    parser = argparse.ArgumentParser(description="Look up movie ratings from a barcode.")
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

    print("Fetching ratings...")

    tmdb_details = get_movie_details_from_tmdb(cleaned_title)

    tmdb_rating = None
    imdb_id = None
    if tmdb_details:
        tmdb_rating = tmdb_details.get('tmdb_rating')
        imdb_id = tmdb_details.get('imdb_id')

    imdb_rating = get_imdb_rating(imdb_id)
    rt_rating = get_rotten_tomatoes_rating(cleaned_title)

    print("\n--- Ratings ---")
    print(f"TMDb: {tmdb_rating if tmdb_rating else 'Not found'}")
    print(f"IMDb: {imdb_rating if imdb_rating else 'Not found'}")
    print(f"Rotten Tomatoes: {rt_rating}")
    print("---------------")

if __name__ == "__main__":
    main()
