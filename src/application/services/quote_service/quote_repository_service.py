from sqlalchemy.orm import Session

from src.application.base import RepositoryServiceBase
from src.domain.entites import Quote, Author


class QuoteRepositoryService(RepositoryServiceBase):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_quote_by_content(self, quote: str) -> Quote | None:
        return Quote(quote)

    def add_quote(self, quote: str, author: Author) -> bool:
        # Logic for checking quote have been added for author -> return False
        # Add quote if not
        return True
