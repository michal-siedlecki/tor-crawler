import requests

from core.settings import settings

PROXY = {"http": settings.TOR_PROXY}


def get(url: str) -> bytes:
    """
    Get response from requested domain using proxy
    """
    response = requests.get(url=url, proxies=PROXY)
    return response.content
