from sqlalchemy.orm import Session

from src.application.base import RepositoryServiceBase
from src.domain.entites import Quote, Author


class QuoteRepositoryService(RepositoryServiceBase):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_quote_by_content(self, quote_content: str) -> Quote | None:
        return self.session.query(Quote).filter(Quote.quote == quote_content).first()

    def add_quote(self, quote_content: str, author: Author) -> bool:
        if self.get_quote_by_content(quote_content) is not None:
            return False

        quote = Quote(quote_content, author)
        self.session.add(quote)
        self.session.commit()

        return True
