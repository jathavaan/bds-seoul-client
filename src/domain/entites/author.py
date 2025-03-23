from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base
from .quote import Quote


class Author(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: str = Column(String(300), nullable=False)
    about_url: str = Column(String(400), nullable=False)

    quotes: list[Quote] = relationship("Author", back_populates="quotes", cascade="all, delete-orphan")

    def __init__(self, name: str, about_url: str, quotes: list[Quote] = None):
        super().__init__()

        if quotes is None:
            quotes = []

        self.name = name
        self.about_url = about_url
        self.quotes = quotes
