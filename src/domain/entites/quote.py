from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base
from src.domain.entites.author import Author


class Quote(Base):
    __tablename__ = "quotes"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quote: str = Column(Text, nullable=False)
    author_id: int = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="quotes")

    def __init__(self, quote: str, author: Author) -> None:
        super().__init__()
        self.quote = quote
        self.author = author
