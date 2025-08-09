import argparse
from movie_lookup import get_movie_title_from_barcode
from rating_services import get_tmdb_rating, get_imdb_rating, get_rotten_tomatoes_rating

def main():
    """
    Main function to get movie ratings from a barcode.
    """
    parser = argparse.ArgumentParser(description="Look up movie ratings from a barcode.")
    parser.add_argument("barcode", help="The UPC barcode of the DVD.")
    args = parser.parse_args()

    print(f"Looking up movie for barcode: {args.barcode}")
    movie_title = get_movie_title_from_barcode(args.barcode)

    if not movie_title:
        print("Could not find a movie for this barcode.")
        return

    print(f"Found movie: {movie_title}")
    print("-" * 20)

    print("Fetching ratings...")
    tmdb_rating = get_tmdb_rating(movie_title)
    imdb_rating = get_imdb_rating(movie_title)
    rt_rating = get_rotten_tomatoes_rating(movie_title)

    print("\n--- Ratings ---")
    print(f"TMDb: {tmdb_rating if tmdb_rating else 'Not found'}")
    print(f"IMDb: {imdb_rating if imdb_rating else 'Not found'}")
    print(f"Rotten Tomatoes: {rt_rating if rt_rating else 'Not found'}")
    print("---------------")

if __name__ == "__main__":
    main()
