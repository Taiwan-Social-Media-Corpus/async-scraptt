import re

from pyquery import PyQuery

from .html_stripper import HTMLStripper


def strip_content(content: PyQuery) -> str:
    """The strip_content function strips the child elements of `content`.

    Args:
        content (PyQuery): a PyQuery object
    Returns:
        a str
    """
    content_clone = (
        content.clone()
        .children()
        .remove('span[class^="article-meta-"]')
        .remove("div.push")
        .end()
        .html()
    )
    stripped_content = HTMLStripper.strip_tags(content_clone)
    return re.sub(r"※ 發信站.*|※ 文章網址.*|※ 編輯.*", "", stripped_content).strip("\r\n-")


def clean_content(content: PyQuery) -> str | None:
    """The clean_content function cleans the post content.

    Args:
        content (PyQuery): a PyQuery object
    Returns:
        a str if the stripped content is not empty, None otherwise.
    """
    stripped_content = strip_content(content)

    if stripped_content == "" or stripped_content is None:
        return None

    quotes = re.findall("※ 引述.*|\n: .*", stripped_content)

    for quote in quotes:
        stripped_content = stripped_content.replace(quote, "")

    return stripped_content.strip("\n ")
