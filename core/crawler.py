import requests

from core.settings import settings

PROXY = {"http": settings.TOR_PROXY}
HEADERS = {"User-Agent": settings.useragent}


def get(url: str) -> str:
    """
    Get response from requested domain using proxy
    """
    response = requests.get(url=url, proxies=PROXY, headers=HEADERS)
    return response.content.decode("utf-8")
