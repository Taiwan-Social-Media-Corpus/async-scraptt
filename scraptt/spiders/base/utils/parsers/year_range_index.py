import re
from typing import Callable

from pyquery import PyQuery
from scrapy import Request
from scrapy.http.response.html import HtmlResponse

from scraptt.config import COOKIES


def parse_year_range_index(
    since: str,
    title_tags: PyQuery,
    response: HtmlResponse,
    callback: Callable,
    self_callback: Callable,
):
    title_tag_list = list(title_tags.items())

    for title_tag in reversed(title_tag_list):
        post_url = title_tag.attr("href")
        timestamp = re.search(r"(\d{10})", post_url).group(1)

        if int(timestamp) < int(since):
            return None

        yield Request(post_url, cookies=COOKIES, callback=callback)

    prev_url = response.dom('.btn.wide:contains("上頁")').attr("href")

    if prev_url:
        yield Request(prev_url, cookies=COOKIES, callback=self_callback)

    return None
