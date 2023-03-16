from pyquery import PyQuery
from scrapy.http.response.html import HtmlResponse

from ..config import PTT


class PyqueryMiddleware:
    """
    The PyqueryMiddleware object injects PyQuery object into Scrapy `response`.
    """

    def process_response(self, *, response: HtmlResponse) -> HtmlResponse:
        response.dom = PyQuery(response.text).make_links_absolute(PTT)
        return response
