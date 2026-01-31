import tiktoken


def pick_fields(source: dict, fields: list[str]) -> dict:
    """
    Pick specified fields from a source dictionary.

    Args:
        source (dict): The source dictionary.
        fields (list): List of field names to pick.

    Returns:
        dict: A new dictionary with only the picked fields.
    """
    return {key: source[key] for key in fields if key in source}



def count_tokens(input: str) -> int:
    """
    Count the number of tokens in the input string using tiktoken for GPT-4.

    Args:
        input (str): The input string to count tokens for.

    Returns:
        int: The number of tokens.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(input)
    return len(tokens)
