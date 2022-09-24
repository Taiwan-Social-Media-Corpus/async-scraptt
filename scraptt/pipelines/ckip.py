from typing import Any, Dict
from ..spiders import PttSpider
from .utils.path import make_file_path
from .utils.ckip.tei_converter import TeiConverter


class CkipPipeline:
    """
    The CkipPipeline object implements CKIP Chinese NLP tools on the scraped item,
    and writes the result to xml.
    """

    def process_item(self, item: Dict[str, Any], spider: PttSpider) -> None:
        file_path = make_file_path(item, spider.data_dir)
        tei_content = TeiConverter(item).convert()

        with open(f"{file_path}.xml", "w") as file:
            file.write(tei_content)
