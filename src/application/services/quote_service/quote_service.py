from src.application.items import QuoteItem
from src.application.services.quote_service.quote_repository_service import QuoteRepositoryService


class QuoteService:
    def remove_quotation_marks(self, quote_item: QuoteItem) -> QuoteItem:
        quote_item["quote"] = str(quote_item["quote"]).lstrip('“').rstrip('”')
        return quote_item

    def to_uppercase(self, quote_item: QuoteItem) -> QuoteItem:
        quote_item["quote"] = str(quote_item["quote"]).upper()
        return quote_item
