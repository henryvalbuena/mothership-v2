"""Utility helpers/tools goes in here"""

import re

from src.helpers.errors import InvalidUserInput


def validate_none_word_input(data: str) -> str:
    """Validates if the data has characters other than letters,
    numbers, or spaces

    Args:
        data: user input
    Raises:
        InvalidUserInput
    Returns:
        user input
    """
    if re.search(r"[^\w ]", data):
        raise InvalidUserInput
    else:
        return data
