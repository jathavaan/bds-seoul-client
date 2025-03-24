from sqlalchemy.orm import Session

from ...base import RepositoryServiceBase


class AuthorRepositoryService(RepositoryServiceBase):
    def __init__(self, session: Session):
        super().__init__(session)
