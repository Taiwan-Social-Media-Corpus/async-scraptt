import asyncio

from pyquery import PyQuery
from scrapy.http.response.html import HtmlResponse

from .validation import CommentsValidator

VOTE_TYPE = {"推": "pos", "噓": "neg", "→": "neu"}


async def create_comment(push_item: tuple[int, PyQuery]) -> dict[str, str | int]:
    """The create_comment_data method creates the comment data.
    Args:
        push_item (tuple): a tuple including comment index and a PyQuery object.
    Returns:
        a dict: {
            'type': 'neu',
            'author': 'LoveMoon',
            'content': '最近面試一些五六年經驗也是只懂皮毛',
            'order': 10
        }
    """
    index, value = push_item
    comment_order = index + 1
    comment_type = value(".push-tag").text()
    author = value(".push-userid").text().split(" ")[0]
    content = value(".push-content").text().lstrip(" :").strip()

    comment = CommentsValidator(
        type=VOTE_TYPE[comment_type],
        author=author,
        content=content,
        order=comment_order,
    )

    return comment.dict()


async def create_comments(response: HtmlResponse) -> list[dict[str, str]]:
    """The parse method parses the comments data.
    Returns:
        a list of dicts
    """
    push_items = response.dom(".push").items()
    tasks = []
    for push_item in enumerate(push_items):
        task = asyncio.create_task(create_comment(push_item))
        tasks.append(task)

    return await asyncio.gather(*tasks)
