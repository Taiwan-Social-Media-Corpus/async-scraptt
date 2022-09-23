import re
import asyncio
from typing import List
from scrapy.http.response.html import HtmlResponse

meta_tag = '//*[@id="main-content"]/div/span[@class="article-meta-tag"]'


async def strip_items(data: List[str]) -> List[str]:
    strip_data = lambda value: value.strip()
    return list(map(strip_data, data))


async def create_meta_data(response: HtmlResponse):
    key_task = strip_items(response.xpath(f"{meta_tag}/text()").getall())
    value_task = strip_items(
        response.xpath(f"{meta_tag}/following-sibling::*/text()").getall()
    )
    return await asyncio.gather(key_task, value_task)


async def get_meta_data(response: HtmlResponse):
    """The get_meta_data function gets the meta data of a post.

    Args:
        response (HtmlResponse): the response to parse
    Returns:
        a dict: {
            '作者': 'scrapy (史窺批)',
            '看板': 'Soft_Job',
            '標題': '[請益] 該不該去讀資工所',
            '時間': 'Fri Aug  5 17:03:40 2022'
        }
    """

    keys, values = await create_meta_data(response)
    return dict(zip(keys, values))
