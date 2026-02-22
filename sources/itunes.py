import requests


ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
MAX_RESULTS = 50


def get_discography(artist_name):
    """
    Retrieve an artist's discography from the iTunes Search API.

    Args:
        artist_name (str): The name of the artist.

    Returns:
        list: A list of dictionaries representing the artist's releases.
              Each dict contains release info like name, release_date, type, etc.
    """
    params = {
        'term': artist_name,
        'media': 'music',
        'entity': 'album',
        'attribute': 'artistTerm',
        'limit': MAX_RESULTS,
    }

    try:
        response = requests.get(ITUNES_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        print(f"iTunes: Request timed out for '{artist_name}'")
        return []
    except requests.RequestException as e:
        print(f"iTunes: Network error retrieving discography for '{artist_name}': {e}")
        return []
    except ValueError as e:
        print(f"iTunes: Failed to parse response for '{artist_name}': {e}")
        return []

    results = data.get('results', [])
    if not results:
        print(f"iTunes: No results found for '{artist_name}'")
        return []

    discography = []
    for item in results:
        release_info = {
            'name': item.get('collectionName', ''),
            'release_date': item.get('releaseDate', ''),
            'album_type': item.get('collectionType', ''),
            'artist': item.get('artistName', ''),
        }
        discography.append(release_info)

    return discography
