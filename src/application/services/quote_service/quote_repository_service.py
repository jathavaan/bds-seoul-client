from sqlalchemy.orm import Session

from ...base import RepositoryServiceBase


class QuoteRepositoryService(RepositoryServiceBase):
    def __init__(self, session: Session):
        super().__init__(session)
