from scrapy.crawler import Crawler

from src.application.services.quote_service.quote_repository_service import QuoteRepositoryService
from src.application.services.quote_service.quote_service import QuoteService
from src.application.services.author_service.author_repository_service import AuthorRepositoryService
from ..spiders import QuoteSpider
from ...application import Container
from ...application.items import QuoteItem


class QuotePipeline:
    quotes_items: list[QuoteItem] = []
    author_repository_service: AuthorRepositoryService
    quote_repository_service: QuoteRepositoryService
    quote_service: QuoteService

    def __init__(
            self,
            author_repository_service: AuthorRepositoryService,
            quote_repository_service: QuoteRepositoryService,
            quote_service: QuoteService
    ) -> None:
        self.author_repository_service = author_repository_service
        self.quote_repository_service = quote_repository_service
        self.quote_service = quote_service

    def process_item(self, item: QuoteItem, spider: QuoteSpider) -> QuoteItem:
        quote_item = self.quote_service.remove_quotation_marks(item)
        quote_item = self.quote_service.to_uppercase(item)

        self.quotes_items.append(quote_item)
        return quote_item

    def open_spider(self, spider: QuoteSpider) -> None:
        print(f"{spider.name} have opened and started crawling {', '.join(spider.start_urls)}")

    def close_spider(self, spider: QuoteSpider) -> None:
        added_authors_count = 0
        added_quote_count = 0

        for quote_item in self.quotes_items:
            author, is_author_added = self.author_repository_service.add_author(
                author_name=quote_item["author"],
                about_author_url=quote_item["about_author_url"]
            )

            is_quote_added = self.quote_repository_service.add_quote(quote_item["quote"], author)

            if is_author_added:
                added_authors_count += 1

            if is_quote_added:
                added_quote_count += 1

        print(f"Added {added_authors_count} new authors and {added_quote_count} new quotes to the database")

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "QuotePipeline":
        container = Container()

        return cls(
            author_repository_service=container.author_repository_service(),
            quote_repository_service=container.quote_repository_service(),
            quote_service=container.quote_service()
        )
