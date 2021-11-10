# Stdlib imports
from urllib.parse import urlparse

# Core Django imports
# Third-party app imports
# Imports from my apps


def is_url(url_):
    """
    check if argument is an url

    :param url_: string of url to check

    :return: boolean
    """
    try:
        result = urlparse(url_)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
