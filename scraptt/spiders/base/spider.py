from abc import (
    ABC,
    abstractmethod,
)
from typing import Optional

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from ..utils.parsers.html import (
    IndexParser,
    LatestIndexParser,
    YearBackwardIndexParser,
    get_title_tags,
)
from ..utils.request import fetch_ptt_boards


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
            return LatestIndexParser(self.logger).parse(response, self.parse_index)

        title_tags = get_title_tags(response)

        if self.since:
            return YearBackwardIndexParser(
                self.since,
                title_tags,
                self.logger,
            ).parse(response, callback=self.parse, self_callback=self.parse_index)

        return IndexParser(title_tags).parse(self.parse)

    @abstractmethod
    def parse(self, response: HtmlResponse, **kwargs):
        pass
