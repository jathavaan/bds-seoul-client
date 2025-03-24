from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base


class Quote(Base):
    __tablename__ = "quotes"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quote: str = Column(Text, nullable=False)
    author_id: int = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Quote", back_populates="author")

    def __init__(self, quote: str) -> None:
        super().__init__()
        self.quote = quote
