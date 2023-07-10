import time
import random
import requests
from typing import Optional

from core import logger, crud
from core.settings import settings


class Crawler:
    proxy = {"http": settings.TOR_PROXY}
    headers = {"User-Agent": settings.useragent}
    accepted_response_codes = [200, 301]
    logger = logger.logger

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get("url")
        self.min_sleep = kwargs.get("min_sleep", 2)
        self.max_sleep = kwargs.get("max_sleep", 5)
        self.retries = kwargs.get("retries", 3)

    def _sleep(self):
        """
        Sleep random time while crawling
        """
        duration = random.randint(self.min_sleep, self.max_sleep)
        self.logger.info(f"Sleeping for {duration} seconds")
        time.sleep(duration)

    def _get(self) -> requests.Response:
        """
        Get response from requested domain using proxy
        """
        response = requests.get(url=self.url, proxies=self.proxy, headers=self.headers)
        if response.status_code in self.accepted_response_codes:
            return response

    def get_page(self) -> Optional[str]:
        """
        Try to get real page content
        """
        response = self._get()
        while self.retries and response.status_code not in self.accepted_response_codes:
            response = self._get()
            self.retries -= 1
        return response.content.decode("utf-8")

    def run(self) -> None:
        """
        Crawl over provided website
        """
