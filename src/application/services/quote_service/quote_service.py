from src.application.services.author_service import AuthorRepositoryService
from src.application.services.quote_service import QuoteRepositoryService


class QuoteService:
    __quote_repository_service: QuoteRepositoryService
    __author_repository_service: AuthorRepositoryService

    def __init__(self, quote_repository_service: QuoteRepositoryService,
                 author_repository_service: AuthorRepositoryService) -> None:
        self.__quote_repository_service = quote_repository_service
        self.__author_repository_service = author_repository_service

    def to_uppercase(self, quote: str) -> str:
        return quote.upper()

    def is_quote_added(self, quote: str) -> bool:
        quote = self.__quote_repository_service.get_quote_by_content(quote)
        return quote is not None
