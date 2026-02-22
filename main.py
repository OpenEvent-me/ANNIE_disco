"""
ANNIE_disco generates a music artist's discography

Uses RAG and an LLM to synthesise a coherent discography using info from
various sources, given only an artist's name.
"""

import os
import sys
from pprint import pprint

import dotenv
import openai

from sources import (musicbrainz, openai as openai_source, spotify)


# ARTIST_NAME = "Fraser Morgan"
# ARTIST_NAME = "Grace Calver"
# ARTIST_NAME = "Thea Gilmore"
# ARTIST_NAME = "Katherine Priddy"
# ARTIST_NAME = "Daniel Stephen Turner"
# ARTIST_NAME = "PET NEEDS"


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
        str: Consolidated discography in schema.org JSON-LD format (MusicRecording and MusicAlbum ).
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
        model=os.getenv('OPENAI_MODEL', 'gpt-5-nano'),
        messages=[
            {"role": "system", "content": "You are a music expert consolidating discography data from multiple sources."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=20000,
        # temperature=0.3,
    )

    return response.choices[0].message.content.strip() # type: ignore


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <artist_name>")
        sys.exit(1)

    artist_name = sys.argv[1]

    # Get discographies from all sources
    sources = {}

    sources['spotify'] = spotify.get_discography(artist_name)
    sources['musicbrainz'] = musicbrainz.get_discography(artist_name)
    sources['openai'] = openai_source.get_discography(artist_name)
    # print(sources)
    # sys.exit(0)
    # Consolidate
    # print("Calling OpenAI to consolidate discography")
    consolidated_discography = consolidate_discography(artist_name, **sources)

    print(consolidated_discography)
