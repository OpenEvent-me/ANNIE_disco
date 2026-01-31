"""
ANNIE_disco generates a music artist's discography

Uses RAG and an LLM to synthesise a coherent discography using info from
various sources, given only an artist's name.
"""

import os
from pprint import pprint

import dotenv
import openai

from sources import (musicbrainz, openai as openai_source, spotify)


ARTIST_NAME = "Fraser Morgan"
ARTIST_NAME = "Grace Calver"
ARTIST_NAME = "Thea Gilmore"
ARTIST_NAME = "Katherine Priddy"
ARTIST_NAME = "Daniel Stephen Turner"
ARTIST_NAME = "PET NEEDS"


dotenv.load_dotenv()


def consolidate_discography(artist_name: str, **sources: dict) -> str:
    """
    Consolidate discographies from multiple sources using OpenAI LLM.

    Args:
        spotify_disc (list): Discography from Spotify.
        musicbrainz_disc (list): Discography from MusicBrainz.
        openai_disc (str): Discography from OpenAI.
        artist_name (str): Name of the artist.

    Returns:
        str: Consolidated discography in schema.org JSON-LD format (MusicMusicRecording and MusicAlbum ).
    """
    prompt = f"""Consolidate the following discography information from multiple sources for the artist '{artist_name}' into a coherent, comprehensive discography.

Spotify data: {sources.get('spotify', [])}

MusicBrainz data: {sources.get('musicbrainz', [])}

OpenAI data: {sources.get('openai', '')}

Synthesize this information into a single, accurate discography using schema.org JSON-LD format. Include MusicAlbum and MusicRecording objects where appropriate. Ensure dates are accurate, remove duplicates, and organize chronologically.

Separate singles and albums into separate lists within the JSON-LD structure, with keys 'albums' and 'singles'.

Return only the JSON-LD objects without any additional text.
"""

    response = openai.chat.completions.create(
        model=os.getenv('OPENAI_MODEL', 'gpt-4'),
        messages=[
            {"role": "system", "content": "You are a music expert consolidating discography data from multiple sources."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip() # type: ignore


if __name__ == "__main__":
    # Get discographies from all sources
    sources = {}

    sources['spotify'] = spotify.get_discography(ARTIST_NAME)
    sources['musicbrainz'] = musicbrainz.get_discography(ARTIST_NAME)
    sources['openai'] = openai_source.get_discography(ARTIST_NAME)

    # Consolidate
    print("Calling OpenAI to consolidate discography")
    consolidated_discography = consolidate_discography(ARTIST_NAME, **sources)

    pprint(consolidated_discography)
