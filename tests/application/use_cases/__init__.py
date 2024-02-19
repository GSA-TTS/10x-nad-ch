import re


def is_valid_date_format(date_str: str) -> bool:
    """
    Verify that a given string matches the following format:
    'January 1, 2024'
    """
    pattern = r"^\w+\s+\d{2},\s+\d{4}$"
    match = re.match(pattern, date_str)
    return bool(match)
