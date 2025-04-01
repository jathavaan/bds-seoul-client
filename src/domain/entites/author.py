from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class Author(Base):
    __tablename__ = "authors"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: str = Column(String(300), nullable=False)
    about_url: str = Column(String(400), nullable=False)

    quotes = relationship("Quote", back_populates="author", cascade="all, delete-orphan")

    def __init__(self, name: str, about_url: str):
        super().__init__()

        self.name = name
        self.about_url = about_url
