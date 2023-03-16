from abc import (
    ABC,
    abstractmethod,
)
from typing import Callable

from scrapy.http.response.html import HtmlResponse


class Parser(ABC):
    """
    The Parser object defines the behaviour for processing the response and
    returning scraped data or more URLs to follow.
    """

    @abstractmethod
    def parse(self, response: HtmlResponse, callback: Callable, **kwargs):
        pass
