from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src import Config
from src.domain.base import Base

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI.value, echo=False)


def create_db_session() -> Session:
    session_maker = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    return session_maker()


def close_db_session(session: Session) -> None:
    session.close()
