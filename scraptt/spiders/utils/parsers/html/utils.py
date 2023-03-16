from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector


def get_title_tags(response: HtmlResponse) -> Selector:
    """The get_title_tags function gets the title tags DOM.
    Args:
        response (HtmlResponse): the scrapy HtmlResponse.
    Returns:
        a set of title anchor tags
    """
    title_css = ".r-ent .title a"

    if response.url.endswith("index.html"):
        return response.dom(".r-list-sep").prev_all(title_css)

    return response.dom(title_css)
