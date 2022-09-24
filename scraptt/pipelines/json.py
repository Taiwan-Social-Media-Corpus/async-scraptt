from io import BufferedWriter
from ..spiders import PttSpider
from typing import Any, Dict, Tuple
from .utils.path import make_file_path
from scrapy.exporters import BaseItemExporter, JsonItemExporter


class JsonPipeline:
    """
    The JsonPipeline object writes the scraped item to json.
    """

    def open_spider(self, spider: PttSpider) -> None:
        self.exporters_list: Dict[str, Tuple[BaseItemExporter, BufferedWriter]] = {}

    def _exporter_for_item(self, item: Dict[str, Any], spider: PttSpider):
        file_path = make_file_path(item, spider.data_dir)

        if file_path not in self.exporters_list:
            file = open(f"{file_path}.json", "wb")
            exporter = JsonItemExporter(file, encoding="utf-8")
            exporter.start_exporting()
            self.exporters_list[file_path] = (exporter, file)

        return self.exporters_list[file_path][0]

    def process_item(self, item: Dict[str, Any], spider: PttSpider) -> Dict[str, Any]:
        exporter = self._exporter_for_item(item, spider)
        exporter.export_item(item)
        return item

    def close_spider(self, spider: PttSpider) -> None:
        for exporter, file in self.exporters_list.values():
            exporter.finish_exporting()
            file.close()
