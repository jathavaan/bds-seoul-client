from sqlalchemy.orm import Session

from src.application.base import RepositoryServiceBase


class QuoteRepositoryService(RepositoryServiceBase):
    def __init__(self, session: Session):
        super().__init__(session)
