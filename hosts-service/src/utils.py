import re
from urllib.parse import urlparse

import requests

DOMAIN_OR_IP_REGEX = re.compile(
    r"^((?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})|"
    r"(?:\d{1,3}\.){3}\d{1,3})$"
)


def validate_url(url: str):
    parsed_url = normalize_url(url)

    if not is_valid_format(parsed_url):
        return ""

    return parsed_url


def normalize_url(url: str):
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url


def is_valid_format(url: str):
    parsed = urlparse(normalize_url(url))
    return bool(parsed.scheme in ("http", "https") and DOMAIN_OR_IP_REGEX.match(parsed.netloc))


def endpoint_exists(url: str):
    try:
        response = requests.head(url)
        return response.status_code < 400
    except requests.RequestException:
        return False
