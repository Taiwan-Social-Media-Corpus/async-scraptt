import re
from typing import Callable

from scrapy import Request
from scrapy.http.response.html import HtmlResponse

from scraptt.config import COOKIES


def parse_latest_index(response: HtmlResponse, callback: Callable):
    prev_url = response.css('.btn.wide:contains("上頁")::attr(href)').get()
    latest_index = int(re.search(r"index(\d{1,6})\.html", prev_url).group(1))
    board = re.search(r"www\.ptt\.cc\/bbs\/([\w\d\-_]{1,30})\/", response.url).group(1)

    for index in range(1, latest_index + 1):
        url = f"https://www.ptt.cc/bbs/{board}/index{index}.html"
        yield Request(url, cookies=COOKIES, callback=callback)
