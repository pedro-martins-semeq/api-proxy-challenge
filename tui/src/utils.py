import re


def is_valid_url(url: str) -> bool:
    return re.match(r"^https?://[^\s]+$", url) is not None
