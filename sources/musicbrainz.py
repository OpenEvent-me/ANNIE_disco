import musicbrainzngs


def get_discography(artist_name):
    """
    Retrieve an artist's discography from MusicBrainz using musicbrainzngs.

    Args:
        artist_name (str): The name of the artist.

    Returns:
        list: A list of dictionaries representing the artist's releases.
              Each dict contains release info like title, date, type, etc.
    """
    # Set user agent for MusicBrainz API
    musicbrainzngs.set_useragent("ANNIE_disco", "0.1a", "https://github.com/OpenEvent-me/ANNIE_disco")

    try:
        # Search for the artist
        result = musicbrainzngs.search_artists(query=f'artist:"{artist_name}"', limit=1)
        if not result['artist-list']:
            # print(f"Musicbrainz: No artist found for '{artist_name}'")
            return []

        artist = result['artist-list'][0]
        artist_id = artist['id']

        # print(f"Musicbrainz: found artist: {artist['name']} (ID: {artist_id})")

        # Get releases for the artist
        releases_result = musicbrainzngs.browse_releases(artist=artist_id, release_type=['album', 'single', 'ep'], limit=50)

        discography = []
        for release in releases_result['release-list']:
            release_info = {
                'title': release.get('title', ''),
                'date': release.get('date', ''),
                'type': release.get('release-group', {}).get('type', ''),
                'id': release.get('id', ''),
                'artist': artist['name']
            }
            discography.append(release_info)

        return discography

    except Exception as e:
        print(f"Error retrieving discography from MusicBrainz: {e}")
        return []

