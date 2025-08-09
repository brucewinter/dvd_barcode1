# Movie Rating Lookup

This project scans a DVD barcode and looks up the movie's rating from TMDB, IMDb, and Rotten Tomatoes.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd movie-rating-lookup
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### TMDB API Key

This project requires a TMDB API key to fetch movie ratings from The Movie Database.

1. Get a free API key from the [TMDb website](https://www.themoviedb.org/documentation/api).
2. Set the API key as an environment variable named `TMDB_API_KEY`.

   - On Linux or macOS:
     ```bash
     export TMDB_API_KEY='your_api_key'
     ```
   - On Windows:
     ```bash
     set TMDB_API_KEY='your_api_key'
     ```

## Usage

Run the `main.py` script with a DVD barcode as a command-line argument:

```bash
python src/main.py <barcode>
```

Example:
```bash
python src/main.py 024543712345
```
