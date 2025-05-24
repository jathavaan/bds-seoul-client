from src.scraper.spiders import QuoteSpider
from src.application.items import QuoteItem


class QuotePipeline:
    def process_item(self, item: QuoteItem, spider: QuoteSpider) -> QuoteItem:
        return item
