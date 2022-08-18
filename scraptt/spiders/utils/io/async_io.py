import asyncio
from typing import Any, Dict
from .io import write_html, write_json, write_tei


async def write_files(
    file_path: str, html_content: str, json_data: Dict[str, Any], tei_content: str
):
    """The write_files function writes files asynchronously.
    
    Args:
        file_path (str): the file path
        html_content (str): the whole html content
        json_data (dict): the ptt post data
        tei_content (str): the tei tags
    """
    return await asyncio.gather(
        *[
            write_html(file_path, html_content),
            write_json(file_path, json_data),
            write_tei(file_path, tei_content),
        ]
    )
