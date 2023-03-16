from typing import (
    Any,
    Dict,
)

from ckip2tei import generate_tei_xml

from ..spiders import PttSpider
from .utils import make_file_path


class CkipPipeline:
    """
    The CkipPipeline object implements CKIP Chinese NLP tools on the scraped item,
    and writes the result to xml.
    """

    def process_item(self, item: Dict[str, Any], spider: PttSpider) -> None:
        file_path = make_file_path(item, spider.data_dir)
        tei_xml = generate_tei_xml(item, "ptt")

        with open(f"{file_path}.xml", "w", encoding="utf-8") as file:
            file.write(tei_xml)
