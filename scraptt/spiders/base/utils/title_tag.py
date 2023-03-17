from pyquery import PyQuery
from scrapy.http.response.html import HtmlResponse


def get_title_tags(response: HtmlResponse) -> PyQuery:
    """The get_title_tags function gets the title tags DOM.
    Args:
        response (HtmlResponse): the scrapy HtmlResponse.
    Returns:
        a set of title anchor tags
    """
    title_css = ".r-ent .title a"
    url: str = response.url

    if url.endswith("index.html"):
        return response.dom(".r-list-sep").prev_all(title_css)

    return response.dom(title_css)
