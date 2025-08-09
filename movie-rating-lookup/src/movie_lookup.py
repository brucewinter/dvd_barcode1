import requests

def get_movie_title_from_barcode(barcode):
    """
    Looks up a movie title from a UPC barcode using the upcitemdb.com API.

    Args:
        barcode (str): The UPC barcode to look up.

    Returns:
        str: The movie title, or None if not found.
    """
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data.get('items'):
            return data['items'][0].get('title')
    except requests.exceptions.RequestException as e:
        print(f"Error looking up barcode: {e}")
    return None
