from io import BufferedWriter
from ...spiders import PttSpider
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
from scrapy.exporters import BaseItemExporter


class BasePipeline:
    def open_spider(self, spider: PttSpider) -> None:
        self.exporters_list: Dict[str, Tuple[BaseItemExporter, BufferedWriter]] = {}

    @abstractmethod
    def _exporter_for_item(
        self, item: Dict[str, Any], spider: PttSpider
    ) -> BaseItemExporter:
        """Define the export type."""
        pass

    def process_item(self, item: Dict[str, Any], spider: PttSpider) -> Dict[str, Any]:
        exporter = self._exporter_for_item(item, spider)
        exporter.export_item(item)
        return item

    def close_spider(self, spider: PttSpider) -> None:
        for exporter, file in self.exporters_list.values():
            exporter.finish_exporting()
            file.close()
