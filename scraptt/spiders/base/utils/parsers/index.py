from typing import Callable

from pyquery import PyQuery
from scrapy import Request

from scraptt.config import COOKIES


def parse_index(title_tags: PyQuery, callback: Callable):
    title_tag_list = list(title_tags.items())

    for title_tag in title_tag_list:
        url = title_tag.attr("href")
        yield Request(url, cookies=COOKIES, callback=callback)
