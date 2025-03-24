from ..spiders import QuoteSpider
from ...application.items import QuoteItem


class QuotePipeline:
    def process_item(self, item: QuoteItem, spider: QuoteSpider) -> None:
        pass
