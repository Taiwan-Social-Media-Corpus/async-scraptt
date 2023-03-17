from abc import (
    ABC,
    abstractmethod,
)
from typing import Optional

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ..utils.request import fetch_ptt_boards
from .utils import get_title_tags
from .utils.parsers import (
    parse_index,
    parse_latest_index,
    parse_year_range_index,
)


class BasePostSpider(Spider, ABC):
    """
    The BasePostSpider object defines the behaviour for crawling and parsing ptt posts.
    """

    allowed_domains = ["ptt.cc"]

    def __init__(
        self,
        *args,
        boards: str,
        data_dir: str = "./data",
        scrape_all: Optional[bool] = None,
        index_from: Optional[int] = None,
        index_to: Optional[int] = None,
        since: Optional[int] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.boards = boards.split(",")
        self.data_dir = data_dir
        self.scrape_all = scrape_all
        self.index_from = index_from
        self.index_to = index_to
        self.since = since
        self.logger.info(f"Targets: {self.boards}")

    def start_requests(self):
        return fetch_ptt_boards(
            self.boards, self.parse_index, self.index_from, self.index_to
        )

    def parse_index(self, response: HtmlResponse):
        if self.scrape_all:
            return parse_latest_index(response, self.parse_index)

        title_tags = get_title_tags(response)

        if self.since:
            return parse_year_range_index(
                self.since, title_tags, response, self.parse, self.parse_index
            )
        return parse_index(title_tags, self.parse)

    @abstractmethod
    def parse(self, response: HtmlResponse, **kwargs):
        pass
