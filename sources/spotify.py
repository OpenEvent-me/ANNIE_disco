import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .utils import pick_fields


# list of keys to pick fro
# m each release/album
RELEASE_FIELDS = [
    'name',
    'release_date',
    'album_type',
]


def get_discography(artist_name):
    """
    Retrieve an artist's discography from Spotify using spotipy.

    Args:
        artist_name (str): The name of the artist.

    Returns:
        list: A list of dictionaries representing the artist's albums.
              Each dict contains album info like name, release_date, etc.
    """
    # Get Spotify credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")

    # Authenticate with Spotify
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    try:
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        print("Error during Spotify authentication:", e)
        return []

    # Search for the artist
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    if not results['artists']['items']: # type: ignore
        print(f"Spotify: No artist found for '{artist_name}'")
        return []

    artist = results['artists']['items'][0] # type: ignore
    artist_id = artist['id']

    # print(f"Spotify: found artist: {artist['name']} (ID: {artist_id})")

    # Get all albums for the artist
    albums = []
    results = sp.artist_albums(artist_id, album_type='album,single', limit=50)
    albums.extend(results['items']) # type: ignore

    # # Handle pagination
    # while results['next']:
    #     results = sp.next(results)
    #     albums.extend(results['items'])

    filtered_albums = [pick_fields(album, RELEASE_FIELDS) for album in albums]

    return filtered_albums
