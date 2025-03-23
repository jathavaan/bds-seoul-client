from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from ..base import Base
from .author import Author


class Quote(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quote: str = Column(Text, nullable=False)

    author: Author = relationship("Quote", back_populates="author")

    def __init__(self, quote: str) -> None:
        super().__init__()
        self.quote = quote
