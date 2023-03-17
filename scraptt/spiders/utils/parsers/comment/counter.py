from collections import Counter

from scrapy.http.response.html import HtmlResponse


async def count_comments(response: HtmlResponse) -> dict[str, int]:
    """The count_comments function counts the total number of comments in a ptt post.

    Args:
        response (HtmlResponse): the response to parse
    Returns:
        a dict: {
            "推 (pos)": 1,
            "噓 (neg)": 2,
            "→ (neu)": 3
        }
    """

    push_tags: list[str] = response.css('span[class*="push-tag"]::text').getall()
    total_comments = [push_tag.strip() for push_tag in push_tags]
    counter = Counter(total_comments)
    ups = counter["推"]
    downs = counter["噓"]
    comments = counter["→"]

    return {"推 (pos)": ups, "噓 (neg)": downs, "→ (neu)": comments}
