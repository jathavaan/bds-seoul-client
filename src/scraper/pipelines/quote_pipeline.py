from scrapy.crawler import Crawler

from ..spiders import QuoteSpider
from ...application import Container
from ...application.items import QuoteItem
from ...application.services.quote_service import QuoteService


class QuotePipeline:
    quotes: list[QuoteItem] = []
    quote_service: QuoteService

    def __init__(self, quote_service: QuoteService) -> None:
        self.quote_service = quote_service

    def process_item(self, item: QuoteItem, spider: QuoteSpider) -> QuoteItem:
        self.quotes.append(item)
        return item

    def open_spider(self, spider: QuoteSpider) -> None:
        pass

    def close_spider(self, spider: QuoteSpider) -> None:
        cleaned_quotes = []
        for quote_item in self.quotes:
            if not self.quote_service.is_quote_added(quote_item["quote"]):
                cleaned_quotes.append(quote_item)

        print(cleaned_quotes)

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "QuotePipeline":
        container = Container()

        return cls(
            quote_service=container.quote_service()
        )
