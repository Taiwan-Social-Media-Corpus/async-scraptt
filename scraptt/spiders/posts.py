import re
import asyncio
from ..items import PostItem
from .base import BasePostSpider
from scrapy.http.response.html import HtmlResponse
from .utils.parsers.posts.meta import get_meta_data
from .utils.parsers.posts.content import ContentCleaner
from .utils.parsers.posts.comment import count_comments, CommentsParser


async def get_post_info(response: HtmlResponse):
    return await asyncio.gather(
        *[
            get_meta_data(response),
            count_comments(response),
            CommentsParser(response).parse(),
        ]
    )


class PttSpider(BasePostSpider):
    """
    The PttSpider object defines the behaviour for crawling and parsing pages for the ptt website.
    """

    name = "ptt"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def parse(self, response: HtmlResponse):
        main_content = response.dom("#main-content")

        if not main_content:
            return None

        body = ContentCleaner(main_content).clean()

        if body is None:
            return None

        post_url = response.url
        board = re.search(r"www\.ptt\.cc\/bbs\/([\w\d\-_]{1,30})\/", post_url).group(1)
        post_id = post_url.split("/")[-1].split(".html")[0]
        timestamp = re.search(r"(\d{10})", response.url).group(1)

        meta_header, comment_counter, comments = asyncio.run(get_post_info(response))
        post_title = meta_header.get("標題", "")
        post_author = meta_header.get("作者", "")

        data = {
            "board": board,
            "post_id": post_id,
            "date": timestamp,
            "title": post_title,
            "author": post_author,
            "body": body,
            "post_vote": comment_counter,
            "comments": comments,
        }

        yield PostItem(**data).dict()
