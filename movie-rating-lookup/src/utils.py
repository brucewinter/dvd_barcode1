import re

def clean_movie_title(title):
    """
    Cleans a movie title by removing extra information like format,
    special editions, etc. This version handles nested parentheses
    and brackets.

    Args:
        title (str): The raw movie title.

    Returns:
        str: The cleaned movie title.
    """
    # Remove nested parentheses by repeatedly removing the innermost ones
    while '(' in title or ')' in title:
        title = re.sub(r'\([^()]*\)', '', title)
        # If the loop doesn't remove anything, break to prevent infinite loops
        # on mismatched parentheses, e.g. "Movie )"
        if '(' not in title and ')' in title or '(' in title and ')' not in title:
            title = title.replace(')', '').replace('(', '') # get rid of them
            break

    # Remove nested brackets
    while '[' in title or ']' in title:
        title = re.sub(r'\[[^\[\]]*\]', '', title)
        if '[' not in title and ']' in title or '[' in title and ']' not in title:
            title = title.replace(']', '').replace('[', '')
            break

    # Remove common retail keywords (case-insensitive)
    keywords = ['4k ultra hd', 'blu-ray', 'dvd', 'boxset', 'steelbook', 'collectors edition']
    for keyword in keywords:
        title = re.sub(r'\b' + re.escape(keyword) + r'\b', '', title, flags=re.IGNORECASE)

    # Remove the word "Trilogy" as it can sometimes confuse search
    title = re.sub(r'\btrilogy\b', '', title, flags=re.IGNORECASE)

    # Clean up extra whitespace
    title = ' '.join(title.split())

    return title.strip()
