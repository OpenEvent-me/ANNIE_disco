import os

import openai


def get_discography(artist_name):
    """
    Retrieve an artist's discography using OpenAI's GPT model.

    Args:
        artist_name (str): The name of the artist.

    Returns:
        str: A synthesized discography description.
    """

    prompt = f"""Provide a detailed discography for the music artist '{artist_name}'. Include album names, release dates, and notable singles.

    Format the discography as a list with each release structure as schema.org MusicRecording and MusicAlbum JSON-LD objects.

    Return only JSON-LD objects without any additional text.
    """

    print("Calling OpenAI with prompt")

    response = openai.chat.completions.create(
        model=os.getenv('OPENAI_MODEL', 'gpt-4'),
        messages=[
            {"role": "system", "content": "You are a knowledgeable music historian."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,

    )

    discography = response.choices[0].message.content.strip() # type: ignore
    return discography

