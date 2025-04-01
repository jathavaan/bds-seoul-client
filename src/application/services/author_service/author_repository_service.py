from sqlalchemy.orm import Session

from src.domain.entites import Author
from ...base import RepositoryServiceBase


class AuthorRepositoryService(RepositoryServiceBase):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_author_by_name(self, name: str) -> Author | None:
        return self.session.query(Author).filter(Author.name == name).first()

    def add_author(self, author_name: str, about_author_url: str) -> tuple[Author, bool]:
        """
        :param author_name:
        :param about_author_url:
        :return: Tuple of author object and boolean. Boolean is True if author was added to DB and False if it already existed
        """
        author = self.get_author_by_name(name=author_name)
        if author is not None:
            return author, False

        author = Author(name=author_name, about_url=about_author_url)
        self.session.add(author)
        self.session.commit()

        return author, True
